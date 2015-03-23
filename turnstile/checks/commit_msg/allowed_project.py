#!/usr/bin/env python
# -*- coding: utf-8 -*-

import turnstile.checks as checks
import turnstile.common.output as output


@checks.Check('Specification Project is allowed')
def check(user_configuration, repository_configuration, commit_message):
    """
    Check if the specification Project is allowed

    >>> import turnstile.models.message as message
    >>> commit = message.CommitMessage('feature/CD-1', 'CD-1 message', 'jira')
    >>> allow_cd = {'allowed-project': {'allowed': ['CD']}}
    >>> result = check(None, allow_cd, commit)
    >>> result.successful
    True
    >>> result.details
    []

    >>> commit = message.CommitMessage('feature/CD-1', 'PF-1 message', 'jira')
    >>> result = check(None, allow_cd, commit)
    >>> result.successful
    False
    >>> result.details
    ["PF isn't allowed on this repository. Please use CD."]

    >>> allow_cd_pf = {'allowed-project': {'allowed': ['CD', 'PF']}}
    >>> commit = message.CommitMessage('feature/CD-1', 'PF-1 message', 'jira')
    >>> result = check(None, allow_cd_pf, commit)
    >>> result.successful
    True
    >>> result.details
    []

    >>> commit = message.CommitMessage('feature/CD-1', 'SHOP-1 message', 'jira')
    >>> result = check(None, allow_cd_pf, commit)
    >>> result.successful
    False
    >>> result.details
    ["SHOP isn't allowed on this repository. Please use one of: CD, PF."]

    >>> commit = message.CommitMessage('feature/CD-1', 'CD-1 message', None)
    >>> result = check(None, allow_cd_pf, commit)
    >>> result.successful
    False
    >>> result.details
    ["Specification format Generic Specification doesn't have projects. Please check your repository configuration."]

    >>> commit = message.CommitMessage('feature/CD-1', 'invalid message', 'jira')
    >>> result = check(None, allow_cd_pf, commit)
    >>> result.successful
    False
    >>> result.details
    ["Specification 'invalid' isn't valid."]

    :param user_configuration: User specific configuration
    :type user_configuration: git_hooks.common.config.UserConfiguration
    :param repository_configuration: Repository specific configuration
    :type repository_configuration: dict
    :param commit_message:
    :type commit_message: git_hooks.models.message.CommitMessage
    :return: If check passed or not
    :rtype: git_hooks.checks.CheckResult
    """
    logger = output.get_sub_logger('commit-msg', 'allowed-project')
    logger.debug('Starting allowed-project check...')
    logger.debug('Commit Message: %s', commit_message)
    specification_format = commit_message.specification.format
    logger.debug('Specification format: %s', specification_format)

    result = checks.CheckResult()
    try:
        project = commit_message.specification.project
    except AttributeError:

        logger.debug("Specification format '%s' doesn't have projects", specification_format)
        template = "Specification format {} doesn't have projects. Please check your repository configuration."
        result.details.append(template.format(specification_format))
        result.successful = False
        return result

    if not project:
        logger.debug("Specification '%s' isn't valid", specification_format)
        template = "Specification '{}' isn't valid."
        result.details.append(template.format(commit_message.specification))
        result.successful = False
        return result

    logger.debug('Project: %s', project)

    check_options = repository_configuration.get('allowed-project', {})
    allowed_projects = check_options.get('allowed', [])
    logger.debug('Allowed projects: %s', allowed_projects)

    is_allowed = project in allowed_projects

    result.successful = is_allowed
    if not is_allowed:
        if len(allowed_projects) == 1:
            template = "{project} isn't allowed on this repository. Please use {allowed}."
        else:
            template = "{project} isn't allowed on this repository. Please use one of: {allowed}."
        result.add_detail(template.format(project=project, allowed=', '.join(allowed_projects)))

    return result
