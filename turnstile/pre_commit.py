#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, absolute_import

import sys

import click
import git

import turnstile.checks as checks
import turnstile.common.config as config
import turnstile.common.output as output
import turnstile.models.staging as staging


@click.command()
def pre_commit():
    """
    This hook is invoked by git commit, and can be bypassed with --no-verify option. It takes no parameter, and is
    invoked before obtaining the proposed commit log message and making a commit.
    Exiting with non-zero status from this script causes the git commit to abort.
    """

    repository = git.Repo()

    user_configuration = config.UserConfiguration()

    logger = output.get_root_logger('pre-commit')
    logger.setLevel(user_configuration.verbosity)
    logger.debug('Starting Pre-Commit Hook')
    logger.debug('Repository Working Dir: %s', repository.working_dir)

    try:
        repository_configuration = config.load_repository_configuration(repository.working_dir)
    except ValueError as e:
        logger.error(e)
        raise click.Abort
    logger.debug('Loaded repository configuration: %s', repository_configuration['CONFIG_FILE'])

    staging_area = staging.StagingArea(repository)
    logger.debug('Changed Files: %d', len(staging_area.changes))

    failed_checks = checks.run_checks('pre-commit', user_configuration, repository_configuration, staging_area)

    if failed_checks:
        s = '' if failed_checks == 1 else 's'
        logger.error('%d check%s failed', failed_checks, s)

    sys.exit(failed_checks)

if __name__ == '__main__':
    pre_commit()
