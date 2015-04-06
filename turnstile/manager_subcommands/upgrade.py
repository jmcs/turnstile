from __future__ import print_function

import distutils.version as du_version

import click
import requests

import turnstile.version as version

PYPI_URL = 'https://pypi.python.org/pypi/zalando-turnstile/json'


def get_pypi_version():
    """
    Gets the latest version from PYPI

    :rtype: distutils.version.LooseVersion | None
    """
    pypi_data = requests.get(PYPI_URL).json()
    project_info = pypi_data.get('info', dict())
    pypi_version = project_info.get('version')
    return du_version.LooseVersion(pypi_version)


@click.command('upgrade')
def cmd():
    """
    Print Turnstile version
    """
    pypi_version = get_pypi_version()
    local_version = du_version.LooseVersion(version.version)
    if pypi_version is None:
        print('Error fetching data from pypi.')
        raise click.Abort
    print('Local Version - ', local_version)
    print('Pypi Version - ', pypi_version)
    if local_version >= pypi_version:
        print('Turnstile is already updated')
    else:
        print('Needs to update')
