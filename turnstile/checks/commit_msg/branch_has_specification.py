#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

import turnstile.checks as checks
import turnstile.common.output as output
import re


@checks.Check('Branch has specification')
def check(user_configuration, repository_configuration, commit_message):
    """
    Check if the branch name includes the specification.

    >>> import turnstile.models.message as message
    >>> commit = message.CommitMessage('feature/CD-1', 'CD-1 message', 'jira')
    >>> result = check(None, {}, commit)
    >>> result.successful, result.details
    (True, [])

    >>> commit = message.CommitMessage('release/R10', 'CD-2 méssage', None)
    >>> result = check(None, {}, commit)
    >>> result.successful, result.details
    (False, ["release/R10 doesn't include a reference to the specification CD-2."])

    You can ignore some branches
    >>> commit = message.CommitMessage('release/R10', 'CD-2 méssage', None)
    >>> result = check(None, {'branch-has-specification': {'exceptions': ['^release/']}}, commit)
    Traceback (most recent call last):
        ...
    CheckIgnore

    And master is always ignored
    >>> commit = message.CommitMessage('master', 'CD-1 méssãg€', None)
    >>> result = check(None, {}, commit)
    Traceback (most recent call last):
        ...
    CheckIgnore

    :param user_configuration: User specific configuration
    :type user_configuration: git_hooks.common.config.UserConfiguration
    :param repository_configuration: Repository specific configuration
    :type repository_configuration: dict
    :param commit_message:
    :type commit_message: git_hooks.models.message.CommitMessage
    :return: If check passed or not
    :rtype: git_hooks.checks.CheckResult
    """
    logger = output.get_sub_logger('commit-msg', 'branch-has-specification')

    logger.debug('Starting branch-has-specification check...')

    result = checks.CheckResult()
    specification = str(commit_message.specification)
    logger.debug('Specification: %s', specification)
    logger.debug('Branch: %s', commit_message.branch)

    check_options = repository_configuration.get('branch-has-specification', {})
    exceptions = check_options.get('exceptions', [])
    exceptions.append('master')  # master is always ignored

    for exception in exceptions:
        logger.debug("Checking if branch matches '%s'", exception)
        if re.match(exception, commit_message.branch):
            logger.debug("'%s' doesn't need to include specification.", commit_message.branch)
            raise checks.CheckIgnore

    has_specification = specification in commit_message.branch

    result.successful = has_specification
    if not has_specification:
        template = "{branch} doesn't include a reference to the specification {spec}."
        result.add_detail(template.format(branch=commit_message.branch, spec=specification))

    return result
