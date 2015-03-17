from __future__ import print_function

import click

import git_hooks.version as version


@click.command('version')
def cmd():
    """
    Print Git Hook version
    """
    print('Zalando Local Git Hooks - ', version.version)
