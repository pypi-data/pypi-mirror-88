#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Git related functions."""

import datetime as dt
import re
import typing

import numpy as np
import pandas as pd
import tqdm

from . import internals, scm
from .internals import log


class _GitLogCollector(scm.ScmLogCollector):
    """Collect log from Git."""

    _args = [
        "log",
        '--pretty=format:"[%h] [%an] [%ad] [%s]"',
        "--date=iso",
        "--numstat",
    ]

    def __init__(self, git_client="git", _pdb=False):
        """Initialize.

        Compiles regular expressions to be used during parsing of log.

        Args:
            git_client: name of git client.
            _pdb: drop in debugger when output cannot be parsed.

        """
        super().__init__()
        self._pdb = _pdb
        self.git_client = git_client
        self.log_moved_re = re.compile(
            r"([-\d]+)\s+([-\d]+)\s+(\S*)\{(\S*) => (\S*)\}(\S*)"
        )

    def parse_path_elem(self, path_elem: str):
        """Parses git output to identify lines added, removed and path.

        Also handles renamed path.

        Args:
            path_elem: path element line.

        Returns:
            Quadruplet of added, removed, rel_path, copy_from_path where
            copy_from_path may be None.

        """
        copy_from_path: typing.Optional[str] = None
        if "{" not in path_elem:
            if "=>" in path_elem:
                added, removed, copy_from_path, _, rel_path = path_elem.split()
            else:
                added, removed, rel_path = path_elem.split()
        else:
            match = self.log_moved_re.match(path_elem)
            if not match:
                raise ValueError(f"{path_elem} not understood")
            added = match.group(1)
            removed = match.group(2)
            rel_path = match.group(3) + match.group(5) + match.group(6)
            rel_path = rel_path.replace("//", "/")
            copy_from_path = (match.group(3) + match.group(4) + match.group(6)).replace(
                "//", "/"
            )
        added_as_int = int(added) if added != "-" else np.nan
        removed_as_int = int(removed) if removed != "-" else np.nan
        return added_as_int, removed_as_int, rel_path, copy_from_path

    def process_entry(self, log_entry):
        """Convert a single xml <logentry/> element to csv rows.

        If the log includes entries about binary files, the added/removed
        columns are set to numpy.nan special value. Only reference the new name
        when a path changes.

        Args:
            log_entry: Git log entry paragraph.

        Yields:
            One or more csv rows.

        """
        try:
            rev, author, date_str, *remainder = log_entry[0][1:-1].split("] [")
        except ValueError:
            log.warning("failed to parse %s", log_entry[0])
            raise
        msg = "] [".join(remainder)
        date = dt.datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S %z")
        if len(log_entry) < 2:
            entry = scm.LogEntry(
                rev,
                author=author,
                date=date,
                path=None,
                message=msg,
                kind="X",
                added=0,
                removed=0,
                copyfrompath=None,
            )
            yield entry
            return
        for path_elem in log_entry[1:]:
            path_elem = path_elem.strip()
            if not path_elem:
                break
            # git log shows special characters in paths to indicate moves.
            try:
                added, removed, relpath, copyfrompath = self.parse_path_elem(path_elem)
            except ValueError as err:
                log.error(f"failed to parse {path_elem}: {err}")
                if self._pdb:
                    import pdb

                    pdb.set_trace()
                continue
            # - indicate binary files.
            entry = scm.LogEntry(
                rev,
                author=author,
                date=date,
                path=relpath,
                message=msg,
                kind="f",
                added=added,
                removed=removed,
                copyfrompath=copyfrompath,
            )
            yield entry
        return

    def process_log_entries(self, text):
        """See :member:`_ScmLogCollector.process_log_entries`."""
        log_entry = []
        for line in text:
            if line.startswith("["):
                if log_entry:
                    yield from self.process_entry(log_entry)
                    log_entry = []
                log_entry.append(line)
                continue
            if not log_entry:
                continue
            log_entry.append(line)
            if line != "":
                continue
        if log_entry:
            yield from self.process_entry(log_entry)
        return

    def get_log(
        self,
        path: str = ".",
        after: dt.datetime = None,
        before: dt.datetime = None,
        progress_bar: tqdm.tqdm = None,
    ) -> pd.DataFrame:
        """Retrieve log from git.

        Args:
            path: location of checked out subversion repository root. Defaults to .
            after: only get the log after time stamp. Defaults to one year ago.
            before: only get the log before time stamp. Defaults to now.
            progress_bar: tqdm.tqdm progress bar.

        Returns:
            pandas.DataFrame with columns matching the fields of
            codemetrics.scm.LogEntry.

        """
        internals.check_run_in_root(path)
        after, before = internals.handle_default_dates(after, before)
        if progress_bar is not None and after is None:
            raise ValueError("progress_bar requires 'after' parameter")
        command = [self.git_client] + self._args
        if after:
            command += ["--after", f"{after:%Y-%m-%d}"]
        if before:
            command += ["--before", f"{before:%Y-%m-%d}"]
        command.append(path)
        results = internals.run(command).split("\n")
        return self.process_log_output_to_df(
            results, after=after, progress_bar=progress_bar
        )


def get_git_log(
    path: str = ".",
    after: dt.datetime = None,
    before: dt.datetime = None,
    progress_bar: tqdm.tqdm = None,
    git_client: str = "git",
    _pdb: bool = False,
) -> pd.DataFrame:
    """Entry point to retrieve git log.

    Args:
        path: location of checked out subversion repository root. Defaults to .
        after: only get the log after time stamp. Defaults to one year ago.
        before: only get the log before time stamp. Defaults to now.
        git_client: git client executable (defaults to git).
        progress_bar: tqdm.tqdm progress bar.
        _pdb: drop in debugger on parsing errors.

    Returns:
        pandas.DataFrame with columns matching the fields of
        codemetrics.scm.LogEntry.

    Example::

        last_year = datetime.datetime.now() - datetime.timedelta(365)
        log_df = cm.git.get_git_log(path='src', after=last_year)

    """
    scm.default_download_func = download
    collector = _GitLogCollector(git_client=git_client, _pdb=_pdb)
    return collector.get_log(
        after=after, before=before, path=path, progress_bar=progress_bar
    )


class _GitFileDownloader(scm.ScmDownloader):
    """Download files from Subversion."""

    def __init__(self, git_client: str = "git"):
        """Initialize downloader.

        Args:
            git_client: name of git client.

        """
        super().__init__(client=git_client, command=["show"])

    def _download(
        self, revision: str, path: typing.Optional[str]
    ) -> scm.DownloadResult:
        """Download specific file and revision from git."""
        command = self.command + [f"{revision}:{path}"]
        content = internals.run(command)
        return scm.DownloadResult(revision, path, content)


def download(data: pd.DataFrame, git_client: str = "git") -> scm.DownloadResult:
    """Downloads files from Subversion.

    Args:
        data: dataframe containing at least a (path, revision) columns to
              identify the files to download.
        git_client: Subversion client executable. Defaults to git.

    Returns:
         list of scm.DownloadResult.

    """
    downloader = _GitFileDownloader(git_client=git_client)
    revision, path = next(data[["revision", "path"]].itertuples(index=False))
    return downloader.download(revision, path)
