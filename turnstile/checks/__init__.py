#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Copyright 2015 Zalando SE

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the
License. You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an
"AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific
language governing permissions and limitations under the License.
"""

import pkg_resources

import turnstile.common.output as output
# we need to import the following modules so import will work on python3


class CheckIgnore(Exception):
    """
    Exception to tell an check should be ignored in a specific case.
    """
    pass


class CheckResult(object):
    def __init__(self, successful=True, details=None):
        """
        :type successful: bool
        :type details: list
        """
        self.successful = successful
        self.details = details or list()

    def add_detail(self, detail):
        """
        Adds detail to a check
        :type detail: str
        """
        self.details.append(detail)


class Check(object):

    """
    Decorator that wraps a check
    """

    def __init__(self, description):
        """
        :param description: Check description
        :type description: str
        """
        self.description = description

    def __call__(self, function):
        function.description = self.description
        return function


def get_checks(hook_name):
    """
    Load all the checks for the hook

    :param hook_name: Which hook is fetching the checks
    :type hook_name: str
    :rtype: [str, FunctionType]
    """
    logger = output.get_sub_logger(hook_name.replace('_', '-'), 'get_checks')

    group_name = 'turnstile.{}'.format(hook_name)
    for entry_point in pkg_resources.iter_entry_points(group_name):
        try:
            module = entry_point.load()
        except ImportError:  # pragma: no cover
            logger.error('%s not found', entry_point.name)
            continue
        check = module.check  # type: FunctionType
        yield entry_point.name, check


def run_checks(hook_name, user_configuration, repository_configuration, check_object, ):
    """
    Runs checks for hooks

    :param hook_name: Which hook is running the checks
    :type hook_name: str
    :param user_configuration: User specific configuration
    :type user_configuration: git_hooks.common.config.UserConfiguration
    :param repository_configuration: Repository specific configuration
    :type repository_configuration: dict
    :param check_object: Object to check, either a CommitMessage or a StagingArea
    :return: Number of failed checks
    :rtype: int
    """

    logger = output.get_sub_logger(hook_name.replace('_', '-'), 'run_checks')
    failed_checks = 0
    checklist = repository_configuration.get('checks', [])
    check_functions = get_checks(hook_name)
    checks_to_run = (check for check_name, check in check_functions if check_name in checklist)
    for check in checks_to_run:

        try:
            result = check(user_configuration, repository_configuration, check_object)
        except CheckIgnore:
            logger.debug('Check was ignored')
            continue

        if result.successful:
            logger.info('✔ %s', check.description)
            for detail in result.details:
                logger.info('  %s', detail)
        else:
            failed_checks += 1
            logger.error('✘ %s', check.description)
            for detail in result.details:
                logger.error('  %s', detail)
    return failed_checks
