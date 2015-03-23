import click

import pathlib

import git

import turnstile.common.output as output


def install_hook(name, path, wrapper_command):
    """
    Installs a hook in path

    :type name: str
    :type path: Path
    :type wrapper_command: str
    """
    logger = output.get_sub_logger('manager-install', 'install_hook')
    logger.debug('Installing %s hook.', name)
    if not path.exists() or click.confirm('{} hook already exists. Do you want to overwrite it?'.format(name)):
        with path.open('wb+') as pre_commit_hook:
            pre_commit_hook.write(wrapper_command.encode('utf-8'))
        path.chmod(0o755)  # -rwxr-xr-x
        logger.info('Installed %s hook', name)
    else:
        logger.info('Skipped %s hook installation.', name)


@click.command('install')
@click.option('-v', 'verbosity', flag_value='DEBUG', help='Use Verbose Mode')
@click.option('-n', 'verbosity', flag_value='INFO', default=True, help='Use Normal Verbosity (default)')
@click.option('-q', 'verbosity', flag_value='WARNING', help='Use Quiet Mode')
def cmd(verbosity):
    """
    Install git hooks in repository
    """

    logger = output.get_root_logger('manager-install')
    logger.setLevel(verbosity)

    logger.info('Installing Git Hooks')
    try:
        repository = git.Repo()
    except git.InvalidGitRepositoryError:
        logger.error('This command should be run inside a git repository')
        exit(-1)

    hook_dir = pathlib.Path(repository.git_dir) / 'hooks'
    pre_commit_path = hook_dir / 'pre-commit'
    commit_msg_path = hook_dir / 'commit-msg'
    install_hook('Pre-Commit', pre_commit_path, 'zalando-turnstile-pre-commit')
    install_hook('Commit-Msg', commit_msg_path, 'zalando-turnstile-commit-msg $1')
