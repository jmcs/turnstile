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

import sys

import click
import git

import turnstile.checks as checks
import turnstile.common.config as config
import turnstile.common.output as output
import turnstile.models.message as message


@click.command()
@click.argument('message_file_path')
def commit_msg(message_file_path):
    """
    This hook is invoked by git commit, and can be bypassed with --no-verify option. It takes a single parameter,
    the name of the file that holds the proposed commit log message.
    Exiting with non-zero status causes the git commit to abort.

    :param message_file_path: the name of the file that holds the proposed commit log message
    :type message_file_path: string
    """

    repository = git.Repo()
    branch = repository.active_branch.name

    user_configuration = config.UserConfiguration()
    logger = output.get_root_logger('commit-msg')
    logger.setLevel(user_configuration.verbosity)

    logger.debug('Starting Commit-Msg Hook')
    logger.debug('Path to commit message file: %s', message_file_path)

    logger.debug('Repository Working Dir: %s', repository.working_dir)
    logger.debug('Current branch: %s', branch)

    try:
        repository_configuration = config.load_repository_configuration(repository.working_dir)
    except ValueError as e:
        logger.error(str(e))
        raise click.Abort
    logger.debug('Loaded repository configuration: %s', repository_configuration['CONFIG_FILE'])

    logger.debug('Opening commit message file')
    try:
        with open(message_file_path) as message_file:
            str_commit_message = message_file.read()
    except IOError:
        logger.error('Commit message file (%s) not found', message_file_path)
        raise click.Abort
    logger.debug('Commit Message: %s', str_commit_message)

    commit_message = message.CommitMessage(branch, str_commit_message)
    logger.debug('Specification: %s', commit_message.specification)

    failed_checks = checks.run_checks('commit_msg', user_configuration, repository_configuration, commit_message)

    if failed_checks:
        s = '' if failed_checks == 1 else 's'
        logger.error('%d check%s failed', failed_checks, s)

    sys.exit(failed_checks)

if __name__ == '__main__':
    commit_msg()  # pragma: no cover
