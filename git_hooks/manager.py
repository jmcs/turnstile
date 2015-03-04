#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

from click import command


@command()
def manager():
    """
    Git Hook Manager
    """

    print('Git Hook Manager')

if __name__ == '__main__':
    manager()
