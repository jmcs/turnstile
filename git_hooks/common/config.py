#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, absolute_import

import logging

import gitconfig

logger = logging.getLogger('githooks.config')


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


class UserConfiguration(object):
    """
    User specific options
    """

    def __init__(self, level='global'):
        self.store = gitconfig.GitConfig(level)

    @property
    def verbosity(self):
        # Try to get logging level from git config otherwise fallback to info
        verbosity = self.store.get('zalando.hooks.verbosity', logging.INFO)
        if not is_valid_log_verbosity(verbosity):
            logger.warning('Invalid Verbosity "%s" falling back to INFO', verbosity)
            verbosity = logging.INFO
        return verbosity

    @verbosity.setter
    def verbosity(self, value):
        """
        Store git hook verbosity in git config

        >>> config=UserConfiguration()
        >>> config.store = dict()  # Don't mess up with real config
        >>> config.verbosity = 'DEBUG'
        >>> config.verbosity
        'DEBUG'

        :param value: new verbosity
        """
        if is_valid_log_verbosity(value):
            self.store['zalando.hooks.verbosity'] = value
        else:
            raise ValueError('"%s" is not a valid verbosity', value)