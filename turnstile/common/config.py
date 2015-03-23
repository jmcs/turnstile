#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, absolute_import

import logging
import pathlib

import gitconfig
import yaml
import yaml.scanner

import turnstile.toolbox.collections as bus_collections

logger = logging.getLogger('turnstile.config')


def is_valid_log_verbosity(verbosity):
    """
    >>> is_valid_log_verbosity('WARNING')
    True

    >>> is_valid_log_verbosity('INFO')
    True

    >>> is_valid_log_verbosity('DEBUG')
    True

    >>> is_valid_log_verbosity('SOMETHINGELSE')
    False

    :type verbosity: str|int
    :rtype: bool
    """
    try:
        logging._checkLevel(verbosity)
        return True
    except (ValueError, TypeError):
        return False


def load_repository_configuration(repository_path):
    """
    Load repository specific configurations adding CONFIG_FILE as a parameter with the load file.
    If hooks.config doesn't exist it returns only  {'CONFIG_FILE': 'DEFAULT'}

    :rtype: dict
    """
    repository_path = pathlib.Path(repository_path)
    config_path = repository_path / '.turnstile.yml'
    try:
        with config_path.open() as config_file:
            # If the configuration file is empty safe_load returns None and we want a dict
            config = yaml.safe_load(config_file) or {}
            config['CONFIG_FILE'] = config_path
    except IOError:
        config = {'CONFIG_FILE': 'DEFAULT'}
    except TypeError:
        raise ValueError('Invalid Repository Configuration')
    except yaml.scanner.ScannerError as e:
        # Try to give a meaningful error if YAML parsing fails
        context = str(e.context_mark).strip()
        error = '{e.problem} {e.context} {context}'.format(e=e, context=context)
        raise ValueError('Invalid Repository Configuration - {}'.format(error))
    return bus_collections.MappingProxy(config)


class UserConfiguration(object):
    """
    User specific options


    >>> config=UserConfiguration()
    >>> config.store = dict()  # Don't mess up with real config
    >>> config.verbosity = 'DEBUG'
    >>> config.verbosity
    'DEBUG'
    >>> config.verbosity = 'INFO'
    >>> config.verbosity
    'INFO'
    >>> config.verbosity = 'OTHER'
    Traceback (most recent call last):
        ...
    ValueError: "OTHER" is not a valid verbosity
    >>> config.store['turnstile.verbosity'] = 'BREAKSTUFF'
    >>> config.verbosity
    'INFO'
    """

    def __init__(self, level='global'):
        self.store = gitconfig.GitConfig(level)

    @property
    def verbosity(self):
        """
        Tries to get logging level from git config, falling back to INFO if it is not set or is an invalid value

        :return: Log Level
        :rtype: str
        """
        verbosity = self.store.get('turnstile.verbosity', 'INFO')
        if not is_valid_log_verbosity(verbosity):
            logger.warning('Invalid Verbosity "%s" falling back to INFO', verbosity)
            verbosity = 'INFO'
        return verbosity

    @verbosity.setter
    def verbosity(self, value):
        """
        Store git hook verbosity in git config

        :type value: str | int
        :param value: new verbosity
        """
        if is_valid_log_verbosity(value):
            self.store['turnstile.verbosity'] = value
        else:
            raise ValueError('"{}" is not a valid verbosity'.format(value))
