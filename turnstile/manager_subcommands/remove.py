import click

import pathlib

import git

import turnstile.common.output as output


def remove_hook(name, path):
    """
    Remove a hook from path

    :type name: str
    :type path: Path
    """

    logger = output.get_sub_logger('manager-remove', 'remove_hook')
    logger.debug('Removing %s hook.', name)
    if not path.exists():
        logger.debug('%s Hook doesn\'t exist.', name)
    elif click.confirm('Are you sure you want to remove {} hook?'.format(name)):
        path.unlink()
        logger.info('Removed %s hook', name)
    else:
        logger.info('Kept %s hook.', name)


@click.command('remove')
@click.option('-v', 'verbosity', flag_value='DEBUG', help='Use Verbose Mode')
@click.option('-n', 'verbosity', flag_value='INFO', default=True, help='Use Normal Verbosity (default)')
@click.option('-q', 'verbosity', flag_value='WARNING', help='Use Quiet Mode')
def cmd(verbosity):
    """
    Remove git hooks from repository
    """

    logger = output.get_root_logger('manager-remove')
    logger.setLevel(verbosity)

    logger.info('Remove Git Hooks')
    try:
        repository = git.Repo()
    except git.InvalidGitRepositoryError:
        logger.error('This command should be run inside a git repository')
        exit(-1)

    hook_dir = pathlib.Path(repository.git_dir) / 'hooks'
    pre_commit_path = hook_dir / 'pre-commit'
    commit_msg_path = hook_dir / 'commit-msg'
    remove_hook('Pre-Commit', pre_commit_path)
    remove_hook('Commit-Msg', commit_msg_path)
