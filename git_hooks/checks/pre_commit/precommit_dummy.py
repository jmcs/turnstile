#!/usr/bin/env python
# -*- coding: utf-8 -*-

import git_hooks.checks as checks
import git_hooks.common.output as output


@checks.Check('Dummy Pre-Commit Check')
def check(staging_area):
    """

    :param commit_message:
    :type commit_message: git_hooks.models.staging.StagingArea
    :return: If check passed or not
    :rtype: bool
    """

    result = checks.CheckResult()

    logger = output.get_sub_logger('pre-commit', 'precommit-dummy')
    with staging_area:
        logger.debug("The changed files are: %s", staging_area.files)
        result.add_detail('The changed files are: {}'.format(staging_area.files))
    return result
