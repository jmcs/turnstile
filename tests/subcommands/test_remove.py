#!/usr/bin/env python
# -*- coding: utf-8 -*-

from click.testing import CliRunner
import git
import pytest
from os.path import abspath, dirname

from turnstile.manager_subcommands.remove import cmd

TEST_FOLDER = dirname(abspath(__file__))


class FakeNonExistingPath(object):
    def __init__(self, *args):
        pass

    def exists(self):
        return False

    def __div__(self, other):
        return self

    def __truediv__(self, other):
        return self


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
    mock = mocker.patch('pathlib.Path')
    return mock


@pytest.fixture
def fake_path_existence(monkeypatch):
    mock2 = monkeypatch.setattr('pathlib.Path', FakeNonExistingPath)
    return mock2


def test_outside_git(fake_no_git):
    runner = CliRunner()
    result = runner.invoke(cmd)
    assert "This command must be executed inside a repository." in result.output
    assert result.exit_code == 1


def test_remove_hook(fake_git, fake_path):
    runner = CliRunner()
    result = runner.invoke(cmd, input='y\ny\n')
    assert "Removed Pre-Commit hook" in result.output
    assert "Removed Commit-Msg hook" in result.output
    assert result.exit_code == 0


def test_dont_remove(fake_git, fake_path):
    runner = CliRunner()
    result = runner.invoke(cmd, input='n\nn\n')
    assert "Kept Pre-Commit hook" in result.output
    assert "Kept Commit-Msg hook" in result.output
    assert result.exit_code == 0


def test_doesnt_exist(fake_git, fake_path_existence):
    fake_path.exists = False
    runner = CliRunner()
    result = runner.invoke(cmd, ['-v'], input='n\nn\n')
    assert "Pre-Commit Hook doesn't exist" in result.output
    assert "Commit-Msg Hook doesn't exist" in result.output
    assert result.exit_code == 0
