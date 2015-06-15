#!/usr/bin/env python
# -*- coding: utf-8 -*-

from click.testing import CliRunner
from turnstile.version import version
from turnstile.manager_subcommands.version import cmd


def test_version():
    runner = CliRunner()
    result = runner.invoke(cmd)
    assert result.output.startswith('Zalando Turnstile')
    assert version in result.output
    assert result.exit_code == 0
