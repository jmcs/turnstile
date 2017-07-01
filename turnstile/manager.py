#!/usr/bin/env python
# -*- coding: utf-8 -*-


from __future__ import absolute_import

import pkg_resources

import click

manager = click.Group()


def get_commands():
    """
    Fetch click commands from extension `turnstile.command` entrypoints.
    The click command functions should be named cmd
    :rtype: Iterator[str, Callable]
    """
    for entry_point in pkg_resources.iter_entry_points('turnstile.commands'):
        try:
            module = entry_point.load()
        except ImportError:
            continue  # ignore broken commands
        command = module.cmd  # type: FunctionType
        yield entry_point.name, command


for name, command in get_commands():
    manager.add_command(command, name=name)


if __name__ == '__main__':
    manager()  # pragma: no cover
