#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Copyright 2015 Zalando SE

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the
License. You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an
"AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific
language governing permissions and limitations under the License.
"""

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
