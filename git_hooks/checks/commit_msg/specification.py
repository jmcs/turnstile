#!/usr/bin/env python
# -*- coding: utf-8 -*-

import git_hooks.checks as checks
import git_hooks.common.output as output


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
    :rtype: bool
    """

    result = checks.CheckResult()
    specification = commit_message.specification
    is_valid = specification.is_valid()

    logger = output.get_sub_logger('commit-msg', 'specification')
    logger.debug('Commit Message: %s', commit_message.message)
    logger.debug('Specification type: %s', specification.type)
    logger.debug("Specification is valid: %s", is_valid)

    result.successful = is_valid
    if not is_valid:
        result.add_detail('{spec} is not a valid {spec.type} specification id.'.format(spec=specification))

    return result
