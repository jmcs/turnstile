#!/usr/bin/env python
# -*- coding: utf-8 -*-


from __future__ import print_function

import click

import turnstile.version as version


@click.command('version')
def cmd():
    """
    Print Turnstile version
    """
    print('Turnstile - ', version.version)
