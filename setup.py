#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

setup(
    name='Zalando Git Hooks',
    packages=['git_hooks'],
    version='0.20150304.1',
    description='Zalando Local Git Hooks',
    author='João Santos',
    author_email='joao.santos@zalando.de',
    url='https://stash.zalando.net/projects/PYMODULES/repos/zalando-githooks/browse',
    install_requires=['click', 'GitPython', 'PyYAML'],
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Version Control',
    ],
    long_description='Zalando Local Git Hooks',
    entry_points={'console_scripts': ['git-hooks = git_hooks.manager:manager',
                  'zalando-local-git-hooks-commit-msg = git_hooks.commit_msg:commit_msg',
                  'zalando-local-git-hooks-pre-commit = git_hooks.pre_commit']},
)

