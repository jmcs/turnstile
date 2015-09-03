#!/usr/bin/env python
# -*- coding: utf-8 -*-

import turnstile.checks as checks
import turnstile.common.output as output
import turnstile.models.specifications as specifications


@checks.Check('Specification is valid')
def check(user_configuration, repository_configuration, commit_message):
    """
    Check if the specification is valid.

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
    allowed_formats = check_options.get('allowed_formats', {'uri'})
    logger.debug("Allowed schemes: %s", allowed_schemes)

    result = checks.CheckResult()
    specification = specifications.get_specification(commit_message.message, allowed_formats, allowed_schemes)
    is_valid_uri = specification.valid

    logger.debug('Specification: %s', specification)
    logger.debug("Specification is valid: %s", is_valid_uri)

    result.successful = is_valid_uri
    if not is_valid_uri:
        result.add_detail('{spec} is not a valid specification.'.format(spec=specification))

    return result
