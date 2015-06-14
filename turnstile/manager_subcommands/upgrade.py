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

from __future__ import print_function

import distutils.version as du_version
import pkg_resources


import click
import pip
import requests


PYPI_URL = 'https://pypi.python.org/pypi/{package}/json'


def get_pypi_version(package):
    """
    Gets the latest version from PYPI

    :rtype: distutils.version.LooseVersion | None
    """
    pypi_data = requests.get(PYPI_URL.format(package=package)).json()
    project_info = pypi_data.get('info', dict())
    pypi_version = project_info.get('version')
    return du_version.LooseVersion(pypi_version)


def upgrade_packages(packages):
    """
    Use pip to upgrade package
    """
    arguments = ['install', '--upgrade']
    arguments.extend(packages)
    pip.main(arguments)


def get_packages():
    """
    Gets a list of packages to be verified.
    """

    for entry_point in pkg_resources.iter_entry_points('turnstile.commands'):
        yield entry_point.dist.version, entry_point.dist.project_name

    for entry_point in pkg_resources.iter_entry_points('turnstile.pre_commit'):
        yield entry_point.dist.version, entry_point.dist.project_name

    for entry_point in pkg_resources.iter_entry_points('turnstile.commit_msg'):
        yield entry_point.dist.version, entry_point.dist.project_name


@click.command('upgrade')
@click.option('--verbose', '-v', is_flag=True)
def cmd(verbose):
    """
    Upgrade Turnstile
    """
    outdated = []
    for package_version, package_name in set(get_packages()):
        pypi_version = get_pypi_version(package=package_name)
        local_version = du_version.LooseVersion(package_version)
        if verbose:
            click.secho('{package_name} {local_version} (PyPi: {pypi_version})'.format(**locals()))
        if local_version < pypi_version:
            outdated.append(package_name)

    if outdated:
        click.secho('The following packages are outdated:', bold=True)
        click.secho('  {packages}'.format(packages=' '.join(outdated)))
        if click.confirm('Do you want to continue?'):
            upgrade_packages(outdated)
    else:
        click.secho('Turnstile is already updated.', bold=True)
