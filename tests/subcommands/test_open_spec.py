#!/usr/bin/env python
# -*- coding: utf-8 -*-

from click.testing import CliRunner
import git
import pytest
from os.path import abspath, dirname

from turnstile.manager_subcommands.open_spec import cmd

TEST_FOLDER = dirname(abspath(__file__))


class FakeCommit(object):
    def __init__(self, hexsha, message):
        self.hexsha = hexsha
        self.message = message


class FakeRemote(object):
    def __init__(self, remote='origin'):
        self.config_reader = {'url': remote}


class FakeRepo(object):
    commits = {
        '000': 'Bad Commit',
        '001': 'https://www.example.com/issue0 Good Commit',
        '002': '#100 Github',
        '003': 'CD-100 Jira'
    }

    def __init__(self, dir=None):
        self.working_dir = TEST_FOLDER

    def commit(self, reference):
        if reference == 'invalid':
            raise git.BadName
        message = self.commits[reference]
        return FakeCommit(reference, message)

    def remote(self, name):
        return FakeRemote('git@github.com:zalando/turnstile.git')


class FakeRepo2(FakeRepo):
    def remote(self, name):
        return FakeRemote('git@example.com:zalando/turnstile.git')


@pytest.fixture()
def fake_no_git(monkeypatch):
    def raiser(*args):
        raise git.InvalidGitRepositoryError

    monkeypatch.setattr(git, 'Repo', raiser)


@pytest.fixture(autouse=True)
def fake_git(monkeypatch):
    monkeypatch.setattr(git, 'Repo', FakeRepo)
    return FakeRepo


@pytest.fixture()
def fake_git2(monkeypatch):
    monkeypatch.setattr(git, 'Repo', FakeRepo2)
    return FakeRepo2


@pytest.fixture(autouse=True)
def fake_webbrowser(monkeypatch, mocker):
    webbrowser_open = mocker.patch('webbrowser.open')
    return webbrowser_open


def test_outside_git(fake_no_git):
    runner = CliRunner()
    result = runner.invoke(cmd, ['000'])
    assert "This command must be executed inside a repository." in result.output
    assert result.exit_code == 1


def test_invalid():
    runner = CliRunner()

    result = runner.invoke(cmd, ['000'])
    assert "That commit doesn't have a valid specification" in result.output
    assert result.exit_code == 1


def test_uri(fake_webbrowser):
    runner = CliRunner()
    result = runner.invoke(cmd, ['001'])
    fake_webbrowser.assert_called_with('https://www.example.com/issue0')
    assert "Opening https://www.example.com/issue0" in result.output
    assert result.exit_code == 0


def test_github(fake_webbrowser, mocker):
    fake_config = mocker.patch('turnstile.common.config.load_repository_configuration')
    fake_config.return_value = {'specification': {'allowed_formats': ['github']}}
    runner = CliRunner()
    result = runner.invoke(cmd, ['002'])
    assert "Opening https://github.com/zalando/turnstile/issues/100" in result.output
    fake_webbrowser.assert_called_with('https://github.com/zalando/turnstile/issues/100')
    assert result.exit_code == 0


def test_github_wrong_remote(fake_webbrowser, mocker, fake_git2):
    fake_config = mocker.patch('turnstile.common.config.load_repository_configuration')
    fake_config.return_value = {'specification': {'allowed_formats': ['github']}}
    runner = CliRunner()
    result = runner.invoke(cmd, ['002'])
    assert "git@example.com:zalando/turnstile.git is not a github repository." in result.output
    assert result.exit_code == 1


def test_jira_not_implemented(fake_webbrowser, mocker):
    fake_config = mocker.patch('turnstile.common.config.load_repository_configuration')
    fake_config.return_value = {'specification': {'allowed_formats': ['jira']}}
    runner = CliRunner()
    result = runner.invoke(cmd, ['003'])
    assert "jira specifications aren't supported yet." in result.output
    assert result.exit_code == 1


def test_invalid_reference():
    runner = CliRunner()

    result = runner.invoke(cmd, ['invalid'])
    assert "'invalid' is not a valid commit reference." in result.output
    assert result.exit_code == 1
