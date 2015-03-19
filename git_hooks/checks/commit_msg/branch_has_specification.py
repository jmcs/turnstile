#!/usr/bin/env python
# -*- coding: utf-8 -*-

import git_hooks.checks as checks
import git_hooks.common.output as output


@checks.Check('Branch has specification')
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
    specification = str(commit_message.specification)

    logger = output.get_sub_logger('commit-msg', 'specification')
    logger.debug('Specification: %s', specification)
    logger.debug('Branch: %s', commit_message.branch)

    # TODO exceptions
    matches_exception = commit_message.branch == 'master'
    has_specification = specification in commit_message.branch

    if matches_exception:
        logger.debug("'%s' doesn't need to include specification.", commit_message.branch)
        raise checks.CheckIgnore

    result.successful = has_specification
    if not has_specification:
        template = "{branch} doesn't include a reference to the specification {spec}."
        result.add_detail(template.format(branch=commit_message.branch, spec=specification))

    return result
