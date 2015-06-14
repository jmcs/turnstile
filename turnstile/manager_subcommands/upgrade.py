#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

import distutils.version as du_version

import click
import pip
import requests

import turnstile.version as version

PYPI_URL = 'https://pypi.python.org/pypi/zalando-core/json'


def get_pypi_version():
    """
    Gets the latest version from PYPI

    :rtype: distutils.version.LooseVersion | None
    """
    pypi_data = requests.get(PYPI_URL).json()
    project_info = pypi_data.get('info', dict())
    pypi_version = project_info.get('version')
    return du_version.LooseVersion(pypi_version)


def upgrade_turnstile():
    """
    Use pip to upgrade turnstile
    """
    # TODO handle extensions updates

    pip.main(['install', '--upgrade', 'zalando-core'])


@click.command('upgrade')
def cmd():
    """
    Upgrade Turnstile
    """
    pypi_version = get_pypi_version()
    local_version = du_version.LooseVersion(version.version)

    if pypi_version is None:
        print('Error fetching data from pypi.')
        raise click.Abort

    if local_version >= pypi_version:
        print('Turnstile is already updated.')
    else:
        print('Local Version - ', local_version)
        print('Pypi Version - ', pypi_version)
        if click.confirm('Do you want to update turnstile?'):
            upgrade_turnstile()
