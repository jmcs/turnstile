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
    >>> commit = message.CommitMessage('master', 'CD-1 message', 'jira')
    >>> result = check(None, {}, commit)
    >>> result.successful, result.details
    (True, [])

    >>> commit = message.CommitMessage('feature/ABC', 'CD-1 message', 'jira')
    >>> result = check(None, {}, commit)
    >>> result.successful, result.details
    (False, ["'feature' type is not allowed. Allowed types are: master."])

    But you can configure it
    >>> allow_feature_release = {'branch-type': {'allowed': ['feature', 'release']}}
    >>> commit = message.CommitMessage('feature/ABC', 'CD-1 message', 'jira')
    >>> result = check(None, allow_feature_release, commit)
    >>> result.successful, result.details
    (True, [])

    >>> allow_feature_release = {'branch-type': {'allowed': ['feature', 'release']}}
    >>> commit = message.CommitMessage('other/ABC', 'CD-1 message', 'jira')
    >>> result = check(None, allow_feature_release, commit)
    >>> result.successful, result.details
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
