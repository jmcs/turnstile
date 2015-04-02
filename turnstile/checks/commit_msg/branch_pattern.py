#!/usr/bin/env python
# -*- coding: utf-8 -*-

import turnstile.checks as checks
import turnstile.common.output as output
import re


@checks.Check('Branch name is valid')
def check(user_configuration, repository_configuration, commit_message):
    """
    Check if the branch name matches the allowed pattern. Master is always allowed

    By default this check only allows master
    >>> import turnstile.models.message as message
    >>> commit = message.CommitMessage('master', 'https://github.com/zalando-bus/turnstile/issues/42 message')
    >>> result = check(None, {}, commit)
    >>> result.successful, result.details
    (True, [])

    >>> commit = message.CommitMessage('feature/42', 'https://github.com/zalando-bus/turnstile/issues/42 message')
    >>> result = check(None, {}, commit)
    >>> result.successful, result.details
    (False, ["feature/42 doesn't match any allowed pattern."])

    But you can add more allowed patterns
    >>> allow_feature_release = {'branch-pattern': {'allowed': ['^feature/', '^release/R']}}
    >>> commit = message.CommitMessage('release/R10', 'https://github.com/zalando-bus/turnstile/issues/42 message')
    >>> result = check(None, allow_feature_release, commit)
    >>> result.successful, result.details
    (True, [])

    >>> allow_feature_release = {'branch-pattern': {'allowed': ['^feature/', '^release/R']}}
    >>> commit = message.CommitMessage('release/R10', 'https://github.com/zalando-bus/turnstile/issues/42 message')
    >>> result = check(None, allow_feature_release, commit)
    >>> result.successful, result.details
    (True, [])

    >>> allow_feature_release = {'branch-pattern': {'allowed': ['^feature/', '^release/R']}}
    >>> commit = message.CommitMessage('release/broken', 'https://github.com/zalando-bus/turnstile/issues/42 message')
    >>> result = check(None, allow_feature_release, commit)
    >>> result.successful, result.details
    (False, ["release/broken doesn't match any allowed pattern."])

    :param user_configuration: User specific configuration
    :type user_configuration: git_hooks.common.config.UserConfiguration
    :param repository_configuration: Repository specific configuration
    :type repository_configuration: dict
    :param commit_message:
    :type commit_message: git_hooks.models.message.CommitMessage
    :return: If check passed or not
    :rtype: git_hooks.checks.CheckResult
    """
    logger = output.get_sub_logger('commit-msg', 'branch-pattern')

    logger.debug('Starting branch-pattern check...')

    result = checks.CheckResult()
    branch = commit_message.branch
    logger.debug('Branch: %s', branch)

    check_options = repository_configuration.get('branch-pattern', {})
    allowed = check_options.get('allowed', [])
    allowed.append('master')  # master is always allowed

    logger.debug('Allowed Patterns: %s', allowed)

    is_allowed = any(re.match(pattern, branch) for pattern in allowed)
    result.successful = is_allowed
    if not is_allowed:
        template = "{branch} doesn't match any allowed pattern."
        result.add_detail(template.format(branch=branch))

    return result
