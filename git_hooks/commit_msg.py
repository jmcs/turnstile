#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, absolute_import

import click

import git_hooks.common.config as config
import git_hooks.common.output as output


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

    user_configuration = config.UserConfiguration()
    logger = output.get_logger('commit-msg', user_configuration.verbosity)
    logger.debug('Starting Commit-Msg Hook')
    logger.debug('Path to commit message file: %s', message_file_path)

    logger.debug('Opening commit message file')
    try:
        with open(message_file_path) as message_file:
            commit_message = message_file.read()
    except FileNotFoundError:
        logger.error('Commit message file (%s) not found', message_file_path)
        raise click.Abort
    logger.debug('Commit Message:\n%s', commit_message)

if __name__ == '__main__':
    commit_msg()
