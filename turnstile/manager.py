#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

import click

import turnstile.manager_subcommands as subcommands

manager = click.Group()
for command in subcommands.commands:
    manager.add_command(command)

if __name__ == '__main__':
    manager()
