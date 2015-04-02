#!/usr/bin/env python
# -*- coding: utf-8 -*-

import turnstile.checks as checks
import turnstile.common.output as output


@checks.Check('Branch type is valid')
def check(user_configuration, repository_configuration, commit_message):
    """
    Check if the branch type is allowed. The branch type is the prefix of the branch name, for example feature/CD-100 is
    a feature branch.

    By default only master is allowed
    >>> import turnstile.models.message as message
    >>> commit_1 = message.CommitMessage('master', 'https://github.com/zalando-bus/turnstile/issues/42 message')
    >>> result_1 = check(None, {}, commit_1)
    >>> result_1.successful, result_1.details
    (True, [])

    >>> commit_2 = message.CommitMessage('feature/ABC', 'https://github.com/zalando-bus/turnstile/issues/42 message')
    >>> result_2 = check(None, {}, commit_2)
    >>> result_2.successful, result_2.details
    (False, ["'feature' type is not allowed. Allowed types are: master."])

    But you can configure it
    >>> allow_feature_release = {'branch-type': {'allowed': ['feature', 'release']}}
    >>> commit_3 = message.CommitMessage('feature/ABC', 'https://github.com/zalando-bus/turnstile/issues/42 message')
    >>> result_3 = check(None, allow_feature_release, commit_3)
    >>> result_3.successful, result_3.details
    (True, [])

    >>> allow_feature_release = {'branch-type': {'allowed': ['feature', 'release']}}
    >>> commit_4 = message.CommitMessage('other/ABC', 'https://github.com/zalando-bus/turnstile/issues/42 message')
    >>> result_4 = check(None, allow_feature_release, commit_4)
    >>> result_4.successful, result_4.details
    (False, ["'other' type is not allowed. Allowed types are: feature, release, master."])

    :param user_configuration: User specific configuration
    :type user_configuration: git_hooks.common.config.UserConfiguration
    :param repository_configuration: Repository specific configuration
    :type repository_configuration: dict
    :param commit_message:
    :type commit_message: git_hooks.models.message.CommitMessage
    :return: If check passed or not
    :rtype: git_hooks.checks.CheckResult
    """
    logger = output.get_sub_logger('commit-msg', 'branch-type')

    logger.debug('Starting branch-type check...')

    result = checks.CheckResult()
    branch = commit_message.branch
    logger.debug('Branch: %s', branch)

    check_options = repository_configuration.get('branch-type', {})
    allowed = check_options.get('allowed', [])

    logger.debug('Allowed Patterns: %s', allowed)

    # add a / after type name because branches should be TYPE/* and master is always allowed
    is_allowed = branch == 'master' or any(branch.startswith(branch_type + '/') for branch_type in allowed)
    result.successful = is_allowed
    if not is_allowed:
        branch_type = branch.split('/').pop(0)
        allowed.append('master')  # make it clear it can also be master
        template = "'{branch_type}' type is not allowed. Allowed types are: {allowed}."
        result.add_detail(template.format(branch_type=branch_type, allowed=', '.join(allowed)))

    return result
