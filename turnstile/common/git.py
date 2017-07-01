#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, absolute_import

from git import InvalidGitRepositoryError, BadName  # noqa
import git
import os

assert BadName  # silence pyflakes


def get_repository(directory=None):
    """
    git.Repo() fails if it's not in the root of the repository so wee need to try the parents to see if we are inside
    a repository

    :rtype: Optional[git.Repo]
    """
    directory = directory or os.getcwd()
    repo = None
    while repo is None and directory != '/':
        try:
            repo = git.Repo(directory)
        except InvalidGitRepositoryError:
            directory = os.path.dirname(directory)
    return repo
