#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os.path import abspath, dirname
import pkg_resources
import pytest
import requests
import json

from turnstile.manager_subcommands.upgrade import get_pypi_version, get_packages, upgrade_packages

TEST_FOLDER = dirname(abspath(__file__))


class FakeResponse:
    def __init__(self, status_code: int, text: str):
        self.status_code = status_code
        self.text = text
        self.ok = status_code == 200

    def json(self):
        return json.loads(self.text)


class FakeEntrypoint:
    def __init__(self, version, project_name):
        self.dist = FakeDistribution(version, project_name)


class FakeDistribution:
    def __init__(self, version, project_name):
        self.version = version
        self.project_name = project_name


@pytest.fixture
def fake_pypi(monkeypatch: '_pytest.monkeypatch.monkeypatch'):
    def fake_get(url: str, params: dict=None):
        if url == "https://pypi.python.org/pypi/turnstile-core-1.0/json":
            return FakeResponse(200, '{"info": {"version": "1.0"}}')
        return url

    monkeypatch.setattr(requests, 'get', fake_get)


@pytest.fixture
def fake_pkg_resources(monkeypatch: '_pytest.monkeypatch.monkeypatch'):
    def fake_iter_entry_points(group):
        if group == 'turnstile.commands':
            return [FakeEntrypoint('1.0', 'package_1')]
        elif group == 'turnstile.pre_commit':
            return [FakeEntrypoint('1.1', 'package_2'), FakeEntrypoint('1.4', 'package_3')]
        elif group == 'turnstile.commit_msg':
            return [FakeEntrypoint('1.0', 'package_1'), FakeEntrypoint('1.4', 'package_4')]

    monkeypatch.setattr(pkg_resources, 'iter_entry_points', fake_iter_entry_points)


def test_get_pypi_version(fake_pypi):
    version = get_pypi_version('turnstile-core-1.0')
    assert version == "1.0"
    assert version.version == [1, 0]


def test_upgrade_packages(mocker):
    pip_main = mocker.patch('pip.main')
    upgrade_packages(['package_1', 'package_2'])
    pip_main.assert_called_once_with(['install', '--upgrade', 'package_1', 'package_2'])


def test_get_packages(fake_pkg_resources):
    packages = set(get_packages())
    assert len(packages) == 4
    assert ('1.0', 'package_1') in packages
    assert ('1.1', 'package_2') in packages
    assert ('1.4', 'package_3') in packages
    assert ('1.4', 'package_4') in packages
