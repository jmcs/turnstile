#!/usr/bin/env python
# -*- coding: utf-8 -*-

import turnstile.checks as checks
import turnstile.common.output as output


@checks.Check('Specification is valid')
def check(user_configuration, repository_configuration, commit_message):
    """
    Check if the specification is valid.

    >>> import turnstile.models.message as message

    Jira tickets are validated according to a specific regex
    >>> commit_1 = message.CommitMessage('something', 'https://github.com/zalando-bus/turnstile/issues/42 m€sságe')
    >>> result_1 = check(None, None, commit_1)
    >>> result_1.successful, result_1.details
    (True, [])

    >>> commit_2 = message.CommitMessage('something', 'invalid-1')
    >>> result_2 = check(None, None, commit_2)
    >>> result_2.successful, result_2.details
    (False, ['invalid-1 is not a valid specification URI.'])

    >>> commit_3 = message.CommitMessage('something', 'Merge stuff')
    >>> result_3 = check(None, None, commit_3)
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

    logger = output.get_sub_logger('commit-msg', 'specification')
    logger.debug('Starting specification check...')
    logger.debug('Commit Message: %s', commit_message.message)

    if commit_message.message.startswith('Merge'):
        logger.debug("Commit is a merge, ignoring.")
        raise checks.CheckIgnore

    result = checks.CheckResult()
    specification = commit_message.specification
    is_valid = specification.valid

    logger.debug('Specification: %s', specification)
    logger.debug("Specification is valid: %s", is_valid)

    result.successful = is_valid
    if not is_valid:
        result.add_detail('{spec} is not a valid specification URI.'.format(spec=specification))

    return result
