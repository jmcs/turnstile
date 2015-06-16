#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Copyright 2015 Zalando SE

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the
License. You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an
"AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific
language governing permissions and limitations under the License.
"""

from __future__ import print_function, absolute_import

from git.exc import InvalidGitRepositoryError
import git
import os


def get_repository(directory=None):
    """
    git.Repo() fails if it's not in the root of the repository so wee need to try the parents to see if we are inside
    a repository

    :rtype: Optional[git.Repo]
    """
    directory = directory or os.getcwd()
    repo = None
    while repo is None and directory != '/':
        print(directory)
        try:
            repo = git.Repo(directory)
        except InvalidGitRepositoryError:
            directory = os.path.dirname(directory)
    return repo
