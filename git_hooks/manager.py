#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, absolute_import

from pathlib import Path
import logging

from click import Group, command
import click
import git

from .version import version

# TODO move this to module
output = logging.getLogger('githooks')
output.setLevel(logging.DEBUG)
output.addHandler(logging.StreamHandler())


@command('install')
def cmd_install():
    """
    Install git hooks in repository
    """

    output.info('Installing Git Hooks')
    try:
        repository = git.Repo()
    except git.InvalidGitRepositoryError:
        # TODO ERROR function
        output.error('This command should be run inside a git repository')
        exit(-1)

    hook_dir = Path(repository.git_dir) / 'hooks'
    pre_commit_path = hook_dir / 'pre-commit'
    commit_msg_path = hook_dir / 'commit-msg'
    install_hook('Pre-Commit', pre_commit_path, 'zalando-local-git-hooks-pre-commit')
    install_hook('Commit-Msg', commit_msg_path, 'zalando-local-git-hooks-commit-msg $1')


def install_hook(name, path, wrapper_command):
    """
    Installs a hook in path

    :type name: str
    :type path: Path
    :type wrapper_command: str
    """

    output.debug('Installing %s Hook.', name)
    if not path.exists() or click.confirm('{} hook already exists. Do you want to overwrite it?'.format(name)):
        with path.open('wb+') as pre_commit_hook:
            pre_commit_hook.write(wrapper_command)
        path.chmod(0o755)  # -rwxr-xr-x
        output.info('Installed %s Hook', name)
    else:
        output.info('Skipped %s Hook installation.', name)


@command('version')
def cmd_version():
    """
    Print Git Hook version
    """

    output.info('Zalando Local Git Hooks - %s', version)

manager = Group()
manager.add_command(cmd_version)
manager.add_command(cmd_install)

if __name__ == '__main__':
    manager()
