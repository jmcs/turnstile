#!/usr/bin/env python
# -*- coding: utf-8 -*-

from click.testing import CliRunner
import git
import pytest
from os.path import abspath, dirname

from turnstile.manager_subcommands.specification import cmd

TEST_FOLDER = dirname(abspath(__file__))


class FakeCommit(object):

    def __init__(self, hexsha, parents, message):
        self.parents = parents
        self.hexsha = hexsha
        self.message = message


class FakeRepo(object):
    commits = {
        '000': ([], 'Bad Commit'),
        '001': (['000'], 'https://www.example.com/issue0 Good Commit'),
        '016': (['000', '001'], 'Merge'),
        '020': (['016'], 'Other Bad Commit'),
        '0f0': (['016'], 'https://www.example.com/issue2 Good Commit'),
        '0f2': (['0f0'], 'https://www.example.com/issue3 Good Commit'),
        '0f4': (['0f2'], 'ftp://www.example.com/issue4 FTP Commit'),
        '0f5': (['0f4'], 'ftp://www.example.com/issue5 FTP Commit'),
    }

    def __init__(self, dir=None):
        self.working_dir = TEST_FOLDER

    def iter_commits(self, revision):
        if '..' in revision:
            min, max = (int(rev, 16) for rev in revision.split('..'))
        else:
            min = 0
            max = int(revision, 16)
        for i in range(min, max):
            commit_id = ('{:03x}'.format(i))
            if commit_id in self.commits:
                parents, message = self.commits.get('{:03x}'.format(i))
                print(parents)
                yield FakeCommit(commit_id, parents, message)


@pytest.fixture
def fake_git(monkeypatch):
    monkeypatch.setattr(git, 'Repo', FakeRepo)
    return FakeRepo


def test_specification(fake_git):
    runner = CliRunner()

    result1 = runner.invoke(cmd, ['0ff'])
    assert '016 Merge' not in result1.output
    assert result1.exit_code == 4

    result2 = runner.invoke(cmd, ['0ff', '-v'])
    assert '016 Merge' in result2.output
    assert result2.exit_code == 4

    result3 = runner.invoke(cmd, ['020..0f2'])
    assert result3.exit_code == 1

    result4 = runner.invoke(cmd, ['021..0f2'])
    assert result4.exit_code == 0
