#!/usr/bin/env python
# -*- coding: utf-8 -*-

import turnstile.checks as checks
import turnstile.common.output as output


@checks.Check('Not committing to master')
def check(user_configuration, repository_configuration, commit_message):
    """
    Prevents commits to master

    >>> import turnstile.models.message as message

    >>> commit = message.CommitMessage('master', 'https://github.com/zalando-bus/turnstile/issues/42 message')
    >>> result = check(None, None, commit)
    >>> result.successful
    False
    >>> result.details
    ['Master branch is protected.']

    :param user_configuration: User specific configuration
    :type user_configuration: git_hooks.common.config.UserConfiguration
    :param repository_configuration: Repository specific configuration
    :type repository_configuration: dict
    :param commit_message:
    :type commit_message: git_hooks.models.message.CommitMessage
    :return: If check passed or not
    :rtype: git_hooks.checks.CheckResult
    """
    logger = output.get_sub_logger('commit-msg', 'protect-master')

    logger.debug('Starting protect-master check...')

    result = checks.CheckResult()
    branch = commit_message.branch
    logger.debug('Branch: %s', branch)

    is_allowed = branch != 'master'
    result.successful = is_allowed
    if not is_allowed:
        result.add_detail("Master branch is protected.")

    return result
