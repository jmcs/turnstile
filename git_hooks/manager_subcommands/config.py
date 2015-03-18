import click

import git_hooks.common.config as config
import git_hooks.common.output as output


@click.command('config')
def cmd():
    """
    Set configuration
    """

    logger = output.get_root_logger('manager-config')
    # TODO: verbosity
    logger.setLevel('DEBUG')

    user_config = config.UserConfiguration()

    # TODO move this to a question cli util
    current_verbosity = user_config.verbosity
    verbosity_levels = ['WARNING', 'INFO', 'DEBUG']
    print('Select the git hook verbosity (Current Value {}):'.format(current_verbosity))
    for i, level in enumerate(verbosity_levels, start=1):
        print('  {i}. {level}'.format(**locals()))
    max_option = len(verbosity_levels)
    option_value = -1
    while not (0 < option_value <= max_option):
        option_value = click.prompt('Please enter an option [1-{n}]'.format(n=max_option), default=2)
    verbosity = verbosity_levels[option_value-1]
    user_config.verbosity = verbosity
