#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

import re

import turnstile.checks as checks
import turnstile.common.output as output


@checks.Check('Branch release is valid')
def check(user_configuration, repository_configuration, commit_message):
    """
    Check if the release of release branches matches a pattern. By default this pattern is ^R(?:\d|\_|\.)+$ but it's
    configurable

    >>> import turnstile.models.message as message
    >>> commit = message.CommitMessage('master', 'https://github.com/zalando-bus/turnstile/issues/42 message')
    >>> result = check(None, {}, commit)
    Traceback (most recent call last):
        ...
    CheckIgnore

    >>> commit = message.CommitMessage('feature/whatever', 'https://github.com/zalando-bus/turnstile/issues/42 message')
    >>> result = check(None, {}, commit)
    Traceback (most recent call last):
        ...
    CheckIgnore

    >>> commit = message.CommitMessage('release/R10_00', 'https://github.com/zalando-bus/turnstile/issues/42 message')
    >>> result = check(None, {}, commit)
    >>> result.successful, result.details
    (True, [])

    >>> commit = message.CommitMessage('release/10_00', 'https://github.com/zalando-bus/turnstile/issues/42 message')
    >>> result = check(None, {}, commit)
    >>> result.successful, len(result.details)
    (False, 1)

    >>> commit = message.CommitMessage('release/10_00', 'https://github.com/zalando-bus/turnstile/issues/42 message')
    >>> result = check(None, {'branch-release': {'pattern': '.*'}}, commit)
    >>> result.successful, result.details
    (True, [])

    :param user_configuration: User specific configuration
    :type user_configuration: git_hooks.common.config.UserConfiguration
    :param repository_configuration: Repository specific configuration
    :type repository_configuration: dict
    :param commit_message:
    :type commit_message: git_hooks.models.message.CommitMessage
    :return: If check passed or not
    :rtype: git_hooks.checks.CheckResult
    """

    logger = output.get_sub_logger('commit-msg', 'branch-release')
    logger.debug('Starting branch-release check...')

    result = checks.CheckResult()
    branch = commit_message.branch
    logger.debug('Branch: %s', branch)
    if not branch.startswith('release/'):
        logger.debug("%s isn't a release branch, ignoring.", branch)
        raise checks.CheckIgnore

    check_options = repository_configuration.get('branch-release', {})
    pattern = check_options.get('pattern', '^R(?:\d|\_|\.)+$')
    branch_type, release = branch.split('/', 1)

    matches_pattern = bool(re.match(pattern, release))
    result.successful = matches_pattern
    if not matches_pattern:
        template = "'{release}' doesn't match '{pattern}'."
        result.add_detail(template.format(release=release, pattern=pattern))

    return result
