#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, absolute_import

from click import Group, command

from .version import version


@command('version')
def cmd_version():
    """
    Git Hook Manager
    """

    print('Zalando Local Git Hooks -', version)

manager = Group()
manager.add_command(cmd_version)

if __name__ == '__main__':
    manager()
