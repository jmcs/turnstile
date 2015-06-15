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

from __future__ import print_function

import click
import git
import sys

import turnstile.models.specifications as specifications


@click.command('specification')
@click.option('--verbose', '-v', is_flag=True)
@click.argument('revision_range', required=False)
def cmd(verbose, revision_range):
    """
    Verifies the specifications of a range of commits.

    This command takes the same revision ranges as ``git log`` to specify which commits are processed

    When using the verbose mode merge commits are printed otherwise they are simply ignored
    """
    # TODO: Load options
    # TODO: unit tests
    # TODO: documentation

    repository = git.Repo()
    commits = list(repository.iter_commits(revision_range))
    invalid = 0
    for commit in commits:
        is_a_merge = len(commit.parents) > 1
        if is_a_merge and not verbose:
            continue
        short_hash = commit.hexsha[:7]
        first_line = commit.message.splitlines()[0]
        specification = specifications.get_specification(commit.message)
        if specification.valid:
            click.secho(' ✔ ', bg='green', fg='white', nl=False)
        elif is_a_merge:
            click.secho('   ', fg='yellow', nl=False, bold=True)
        else:
            invalid += 1
            click.secho(' ✘ ', bg='red', fg='white', nl=False)
        click.secho(' {} '.format(short_hash), fg='white' if is_a_merge else 'yellow', nl=False, dim=is_a_merge)
        click.secho(first_line, dim=is_a_merge)
    if invalid:
        if invalid == 1:
            message = '1 commit has invalid specification.'
        else:
            message = '{n} commits have invalid specifications.'.format(n=invalid)
        click.secho(message, fg='red', bold=True)
    sys.exit(invalid)
