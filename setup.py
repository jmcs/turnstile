#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand

from turnstile.version import version


class PyTest(TestCommand):
    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.cov = None
        self.pytest_args = ['--cov', 'turnstile',
                            '--cov-report', 'term-missing',
                            '--doctest-modules', 'turnstile', 'tests']

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest

        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


setup(
    name='turnstile-core',
    packages=find_packages(),
    version=version,
    description='Turnstile - Zalando Local Git Hooks',
    author='Zalando SE',
    url='https://github.com/zalando/turnstile',
    license='Apache License Version 2.0',
    install_requires=['click', 'GitPython', 'pathlib', 'PyYAML', 'rfc3986', 'MapGitConfig', 'requests', 'pip',
                      'pyrsistent'],
    tests_require=['pytest-cov', 'pytest', 'pytest-mock', ],
    cmdclass={'test': PyTest},
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Version Control',
    ],
    long_description='Turnstile - Zalando Local Git Hooks',
    entry_points={'console_scripts': ['turnstile = turnstile.manager:manager',
                                      'zalando-turnstile-commit-msg = turnstile.commit_msg:commit_msg',
                                      'zalando-turnstile-pre-commit = turnstile.pre_commit:pre_commit'],
                  'turnstile.commands': ['config = turnstile.manager_subcommands.config',
                                         'install = turnstile.manager_subcommands.install',
                                         'open-spec = turnstile.manager_subcommands.open_spec',
                                         'remove = turnstile.manager_subcommands.remove',
                                         'specification = turnstile.manager_subcommands.specification',
                                         'upgrade = turnstile.manager_subcommands.upgrade',
                                         'version = turnstile.manager_subcommands.version'],
                  'turnstile.commit_msg': ['branch_pattern = turnstile.checks.commit_msg.branch_pattern',
                                           'branch_release = turnstile.checks.commit_msg.branch_release',
                                           'branch_type = turnstile.checks.commit_msg.branch_type',
                                           'protect_master = turnstile.checks.commit_msg.protect_master',
                                           'specification = turnstile.checks.commit_msg.specification']}
)
