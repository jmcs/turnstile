#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

import importlib
import pkgutil

# Fetch click commands from submodules from git_hooks.manager_subcommands
# The click command functions should be named cmd

commands = []
for loader, module_name, is_pkg in pkgutil.walk_packages(__path__):
    name = '.' + module_name
    # import submodule git_hooks.manager_subcommands.*
    sub_module = importlib.import_module(name, 'turnstile.manager_subcommands')
    try:
        commands.append(sub_module.cmd)
    except AttributeError:
        print('Error loading', module_name)
        pass
