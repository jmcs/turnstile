#!/usr/bin/env python
# -*- coding: utf-8 -*-

from turnstile.checks import get_checks
from turnstile.manager import get_commands

CORE_COMMIT_MSG_CHECKS = ['branch_pattern', 'branch_release', 'branch_type', 'protect_master', 'specification']
CORE_SUBCOMMANDS = ['config', 'install', 'remove', 'specification', 'upgrade', 'version']


def test_checks():
    checks = dict(get_checks('commit_msg'))
    for check_name in CORE_COMMIT_MSG_CHECKS:
        assert check_name in checks


def test_subcommands():
    subcommands = dict(get_commands())
    for subcommand_name in CORE_SUBCOMMANDS:
        assert subcommand_name in subcommands
