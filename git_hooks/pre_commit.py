#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

from click import command


@command()
def pre_commit():
    """
    Pre commit hook
    """

    print('pre-commit hook')

if __name__ == '__main__':
    pre_commit()
