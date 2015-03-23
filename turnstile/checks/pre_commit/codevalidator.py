#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

import subprocess
import re

import turnstile.checks as checks
import turnstile.common.output as output


def remove_temporary_path(codevalidator_output, temporary__dir_path):
    """
    Removes the temporary dir path from the file paths

    >>> remove_temporary_path('/tmp/test/file.a ERROR', '/tmp/test')
    'file.a ERROR'

    :param codevalidator_output: Raw codevalidator output
    :type codevalidator_output: str
    :param temporary__dir_path:
    :type temporary__dir_path: pathlib.Path
    :return: codevalidator_output with paths relative to the root directory
    """

    regular_expression = '^{temp_dir}/'.format(temp_dir=re.escape(str(temporary__dir_path)))
    regex = re.compile(regular_expression)
    lines = [regex.sub('', line, 1) for line in codevalidator_output.splitlines()]
    return '\n'.join(lines)


@checks.Check('Codevalidator Check')
def check(user_configuration, repository_configuration, staging_area):
    """
    Codevalidator check

    :param user_configuration: User specific configuration
    :type user_configuration: git_hooks.common.config.UserConfiguration
    :param repository_configuration: Repository specific configuration
    :type repository_configuration: dict
    :param staging_area:
    :type staging_area: git_hooks.models.staging.StagingArea
    :return: If check passed or not
    :rtype: bool
    """

    result = checks.CheckResult()

    logger = output.get_sub_logger('pre-commit', 'codevalidator')
    logger.debug('Starting Codevalidator check...')
    if not staging_area.changes:
        logger.debug('No files to check.')
        raise checks.CheckIgnore

    codevalidator_rc = staging_area.working_dir / '.codevalidatorrc'

    with staging_area:
        arguments = ['codevalidator', '-v']
        arguments.extend(str(path) for path in staging_area.files)

        if codevalidator_rc.is_file:
            arguments.extend(['-c', str(codevalidator_rc.resolve())])

        logger.debug('Command Arguments: %s', arguments)

        process = subprocess.Popen(arguments, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        logger.debug('Standard Output: %s', stdout)
        logger.debug('Standard Error: %s', stderr)

        codevalidator_output = stdout+stderr
        result.successful = not codevalidator_output
        if not result.successful:
            result.details.append(remove_temporary_path(codevalidator_output, staging_area.temporary_directory))

    return result
