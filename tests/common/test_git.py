#!/usr/bin/env python
# -*- coding: utf-8 -*-

from git.exc import InvalidGitRepositoryError
import git
import pytest

from turnstile.common.git import get_repository


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
        if dir == '/repos/good_repo':
            return
        else:
            raise InvalidGitRepositoryError


@pytest.fixture
def fake_git(monkeypatch):
    monkeypatch.setattr(git, 'Repo', FakeRepo)
    return FakeRepo


def test_get_repository(fake_git):
    assert get_repository('/repos/good_repo') is not None
    assert get_repository('/repos/good_repo/subfolder') is not None
    assert get_repository('/repos/bad_repo/') is None
    assert get_repository('/repos/bad_repo/subfolder') is None
