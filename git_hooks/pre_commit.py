#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

from click import command

import git_hooks.common.config as config
import git_hooks.common.output as output


@command()
def pre_commit():
    """
    This hook is invoked by git commit, and can be bypassed with --no-verify option. It takes no parameter, and is
    invoked before obtaining the proposed commit log message and making a commit.
    Exiting with non-zero status from this script causes the git commit to abort.
    """

    user_configuration = config.UserConfiguration()
    logger = output.get_logger('pre-commit', user_configuration.verbosity)
    logger.debug('Starting Pre-Commit Hook')

if __name__ == '__main__':
    pre_commit()
