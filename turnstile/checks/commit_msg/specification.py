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
    >>> result_1 = check(None, {}, commit_1)
    >>> result_1.successful, result_1.details
    (True, [])

    >>> commit_2 = message.CommitMessage('something', 'invalid-1')
    >>> result_2 = check(None, {}, commit_2)
    >>> result_2.successful, result_2.details
    (False, ['invalid-1 is not a valid specification URI.'])

    >>> commit_3 = message.CommitMessage('something', 'Merge stuff')
    >>> result_3 = check(None, {}, commit_3)
    Traceback (most recent call last):
        ...
    CheckIgnore

    >>> commit_4 = message.CommitMessage('something', 'ftp://example.com/spec')
    >>> result_4 = check(None, {'specification': {'allowed_schemes': ['https']}}, commit_4)
    >>> result_4.successful, result_4.details
    (False, ['ftp is not allowed. Allowed schemes are: https'])

    >>> commit_5 = message.CommitMessage('something', 'ftp://example.com/spec')
    >>> result_5 = check(None, {'specification': {'allowed_schemes': ['https', 'ftp']}}, commit_5)
    >>> result_5.successful, result_5.details
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

    logger = output.get_sub_logger('commit-msg', 'specification')
    logger.debug('Starting specification check...')
    logger.debug('Commit Message: %s', commit_message.message)

    if commit_message.message.startswith('Merge'):
        logger.debug("Commit is a merge, ignoring.")
        raise checks.CheckIgnore

    check_options = repository_configuration.get('specification', {})
    allowed_schemes = check_options.get('allowed_schemes', ['https', 'offline'])
    logger.debug("Allowed schemes: %s", allowed_schemes)

    result = checks.CheckResult()
    specification = commit_message.specification
    is_valid_uri = specification.valid
    is_valid_scheme = specification.uri.scheme in allowed_schemes

    logger.debug('Specification: %s', specification)
    logger.debug("Specification is valid: %s", is_valid_uri)

    result.successful = is_valid_uri and is_valid_scheme
    if not is_valid_uri:
        result.add_detail('{spec} is not a valid specification URI.'.format(spec=specification))
    elif not is_valid_scheme:
        template = '{scheme} is not allowed. Allowed schemes are: {allowed}'
        result.add_detail(template.format(scheme=specification.uri.scheme, allowed=', '.join(allowed_schemes)))

    return result
