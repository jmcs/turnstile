#!/usr/bin/env python
# -*- coding: utf-8 -*-

from click.testing import CliRunner
from os.path import abspath, dirname
import pkg_resources
import pytest
import requests
import json

from turnstile.manager_subcommands.upgrade import get_pypi_version, get_packages, upgrade_packages, cmd

TEST_FOLDER = dirname(abspath(__file__))


class FakeResponse:
    def __init__(self, status_code, text):
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
def fake_pypi(monkeypatch):
    def fake_get(url):
        if url == "https://pypi.python.org/pypi/package_1/json":
            return FakeResponse(200, '{"info": {"version": "1.0"}}')
        elif url == "https://pypi.python.org/pypi/package_2/json":
            return FakeResponse(200, '{"info": {"version": "2.0"}}')
        elif url == "https://pypi.python.org/pypi/package_3/json":
            return FakeResponse(200, '{"info": {"version": "2.0"}}')
        elif url == "https://pypi.python.org/pypi/package_4/json":
            return FakeResponse(200, '{"info": {"version": "1.4"}}')
        return url

    monkeypatch.setattr(requests, 'get', fake_get)


@pytest.fixture
def fake_pkg_resources(monkeypatch):
    def fake_iter_entry_points(group):
        if group == 'turnstile.commands':
            return [FakeEntrypoint('1.0', 'package_1')]
        elif group == 'turnstile.pre_commit':
            return [FakeEntrypoint('1.1', 'package_2'), FakeEntrypoint('1.4', 'package_3')]
        elif group == 'turnstile.commit_msg':
            return [FakeEntrypoint('1.0', 'package_1'), FakeEntrypoint('1.4', 'package_4')]

    monkeypatch.setattr(pkg_resources, 'iter_entry_points', fake_iter_entry_points)


def test_get_pypi_version(fake_pypi):
    version = get_pypi_version('package_1')
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

def test_specification(mocker, fake_pkg_resources, fake_pypi):
    pip_main = mocker.patch('pip.main')
    runner = CliRunner()

    result1 = runner.invoke(cmd, input='y\n')
    assert 'package_2' in result1.output
    assert 'package_3' in result1.output
    assert 'package_1' not in result1.output
    assert 'package_4' not in result1.output
    pip_args = pip_main.call_args[0][0]
    assert 'package_2' in pip_args
    assert 'package_3' in pip_args
    assert 'package_1' not in pip_args
    assert 'package_4' not in pip_args
    pip_main.reset_mock()

    result2 = runner.invoke(cmd, ['-v'], input='y\n')
    assert 'package_2' in result2.output
    assert 'package_3' in result2.output
    assert 'package_1' in result2.output
    assert 'package_4' in result2.output
    pip_args = pip_main.call_args[0][0]
    assert 'package_2' in pip_args
    assert 'package_3' in pip_args
    assert 'package_1' not in pip_args
    assert 'package_4' not in pip_args
    pip_main.reset_mock()

    pkg_resources.iter_entry_points = lambda x: []

    result3 = runner.invoke(cmd, input='y\n')
    assert result3.output == 'Turnstile is already updated.\n'
    assert not pip_main.called

