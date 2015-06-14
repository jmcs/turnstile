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
        self.pytest_args = ['--cov', 'turnstile', '--cov-report', 'term-missing', '--doctest-modules', 'turnstile']

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


setup(
    name='zalando-turnstile',
    packages=find_packages(),
    version=version,
    description='Turnstile - Zalando Local Git Hooks',
    author='Zalando SE',
    url='https://github.com/zalando-bus/turnstile',
    license='Apache License Version 2.0',
    install_requires=['click', 'GitPython', 'pathlib', 'PyYAML', 'codevalidator', 'rfc3986', 'MapGitConfig',
                      'requests', 'pip'],
    tests_require=['pytest-cov', 'pytest'],
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
                  'turnstile.commands': ['codevalidator = turnstile.manager_subcommands.codevalidator',
                                         'config = turnstile.manager_subcommands.config',
                                         'install = turnstile.manager_subcommands.install',
                                         'remove = turnstile.manager_subcommands.remove',
                                         'upgrade = turnstile.manager_subcommands.upgrade',
                                         'version = turnstile.manager_subcommands.version'],}
)
