import click

import turnstile.common.config as config


@click.command('config')
def cmd():
    """
    Set configuration
    """
    # TODO implement local and global

    user_config = config.UserConfiguration()

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
