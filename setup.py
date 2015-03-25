#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

from turnstile.version import version

setup(
    name='zalando-turnstile',
    packages=find_packages(),
    version=version,
    description='Turnstile - Zalando Local Git Hooks',
    author='Zalando SE',
    url='https://github.com/zalando-bus/turnstile',
    license='Apache License Version 2.0',
    install_requires=['click', 'GitPython', 'pathlib', 'PyYAML', 'codevalidator', 'rfc3986'],
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
                                      'zalando-turnstile-pre-commit = turnstile.pre_commit:pre_commit']},
)
