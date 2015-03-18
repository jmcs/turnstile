#!/usr/bin/env python
# -*- coding: utf-8 -*-

import git_hooks.checks as checks
import git_hooks.common.output as output


@checks.Check('Dummy Message Check')
def check(user_configuration, repository_configuration, commit_message):
    """
    Dummy check

    :param user_configuration: User specific configuration
    :type user_configuration: git_hooks.common.config.UserConfiguration
    :param repository_configuration: Repository specific configuration
    :type repository_configuration: dict
    :param commit_message:
    :type commit_message: git_hooks.models.message.CommitMessage
    :return: If check passed or not
    :rtype: bool
    """

    result = checks.CheckResult()

    logger = output.get_sub_logger('commit-msg', 'message-dummy')
    logger.debug("Commit message is '%s' and I think it's ok", commit_message.message)
    result.add_detail('Commit Message is: {}'.format(commit_message.message))
    return result
