#!/usr/bin/env python
# -*- coding: utf-8 -*-

from click.testing import CliRunner
import git
import pytest
from os.path import abspath, dirname

from turnstile.manager_subcommands.install import cmd

TEST_FOLDER = dirname(abspath(__file__))


class FakeRepo(object):
    def __init__(self, dir=None):
        self.working_dir = TEST_FOLDER
        self.git_dir = '.git'


@pytest.fixture
def fake_git(monkeypatch):
    monkeypatch.setattr(git, 'Repo', FakeRepo)
    return FakeRepo


@pytest.fixture()
def fake_no_git(monkeypatch):
    def raiser(*args):
        raise git.InvalidGitRepositoryError

    monkeypatch.setattr(git, 'Repo', raiser)


@pytest.fixture
def fake_path(mocker):
    m = mocker.patch('pathlib.Path')
    return m


def test_outside_git(fake_no_git):
    runner = CliRunner()
    result = runner.invoke(cmd)
    assert "This command must be executed inside a repository." in result.output
    assert result.exit_code == 1


def test_already_existed(fake_git, fake_path):
    runner = CliRunner()
    result = runner.invoke(cmd, input='y\ny\n')
    assert "Pre-Commit hook already exists. Do you want to overwrite it?" in result.output
    assert "Installed Pre-Commit hook" in result.output
    assert "Commit-Msg hook already exists. Do you want to overwrite it?" in result.output
    assert "Installed Commit-Msg hook" in result.output
    assert result.exit_code == 0


def test_dont_install(fake_git, fake_path):
    runner = CliRunner()
    result = runner.invoke(cmd, input='n\nn\n')
    assert "Pre-Commit hook already exists. Do you want to overwrite it?" in result.output
    assert "Skipped Pre-Commit hook installation" in result.output
    assert "Commit-Msg hook already exists. Do you want to overwrite it?" in result.output
    assert "Skipped Commit-Msg hook installation" in result.output
    assert result.exit_code == 0
