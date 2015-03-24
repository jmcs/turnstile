#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Classes to represent the git repository staging area
"""

import itertools
import pathlib
import tempfile
import shutil


class StagingArea(object):
    """
    Class to represent the staging area as an whole.
    It should be used as context manager (with the "with" statement).
    """

    def __init__(self, repository):
        """
        :param repository: GitPython Repository
        :rtype repository: git.repo.base.Repo
        """

        self.temporary_directory = None
        self.files = []  # this will be populated with the temporary files

        if repository.active_branch.is_valid():
            diff = repository.head.commit.diff()
            added_changes = diff.iter_change_type('A')
            modified_changes = diff.iter_change_type('M')
            self.changes = list(itertools.chain(added_changes, modified_changes))
        else:
            # if the branch still doesn't have commits the diff will fail
            self.changes = []

        self.working_dir = pathlib.Path(repository.working_dir)

    def __enter__(self):
        """
        Enter context manager and create a temporary directory
        """
        self.temporary_directory = pathlib.Path(tempfile.mkdtemp())
        self.files = [self.create_temp_file(diff) for diff in self.changes]
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Remove temporary directory on exit
        """
        self.files = []
        shutil.rmtree(str(self.temporary_directory), ignore_errors=True)
        self.temporary_directory = None

    def create_temp_file(self, file_diff):
        """
        Creates a temporary file based on a GitPython file diff
        This method replicates the original project structure and creates a file with the original name

        :param file_diff: Diff for file
        :type file_diff: git.diff.Diff
        """

        if not self.temporary_directory:
            raise ValueError('StagingArea not entered')

        new_version = file_diff.b_blob
        original_relative_path = new_version.path
        content = new_version.data_stream.stream.read()

        temporary_path = self.temporary_directory / original_relative_path
        if not temporary_path.parent.exists():
            temporary_path.parent.mkdir(parents=True)
        with temporary_path.open('wb') as temporary_file:
            temporary_file.write(content)
        return temporary_path
