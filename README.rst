.. image:: https://travis-ci.org/zalando/turnstile.svg?branch=master
   :target: https://travis-ci.org/zalando/turnstile
   :alt: Build Status

.. image:: https://coveralls.io/repos/zalando/turnstile/badge.svg?branch=master
  :target: https://coveralls.io/r/zalando/turnstile?branch=master
  :alt: Code Coverage

.. image:: https://img.shields.io/pypi/v/turnstile-core.svg
   :target: https://pypi.python.org/pypi/turnstile-core/
   :alt: Latest PyPI version

.. image:: https://img.shields.io/pypi/l/turnstile-core.svg
   :target: https://github.com/zalando/turnstile/blob/master/LICENSE
   :alt: License


Turnstile - Zalando Local Git Hooks
===================================

Configurable local git hooks.

Installation
------------
You can install turnstile using pip:

    # pip install turnstile-core

Alternative you can install it using setup.py

    # setup.py install

Adding and removing turnstile from a repository
-----------------------------------------------
To use turnstile in a repository you have to run ``turnstile install`` inside the repository.

To remove turnstile from a repository you have to run ``turnstile remove`` inside the repository.

Configuring turnstile
---------------------
You can configure the global hook behaviour by running ``turnstile config``.

Currently you can only configure the hook verbosity.

Repository Configuration
------------------------
To use Turnstile you need to add a configuration file named ``.turnstile.yml`` to your repository.

You can find an example configuration in `turnstile repository <turnstile.yml.example>`_ and you can read can learn more
about the configuration options in the `documentation <rtd_>`_.

Adding subcommands
------------------
Turnstile looks for command extensions in ``turnstile.commands`` entry points.

To make a new subcommand create a `click <http://click.pocoo.org>`_ command named ``cmd`` and add the module with command
to your setup.py entry points in the 'turnstile.commands' group.

More information
-----------------
To learn more check `Turnsile's Documentation <rtd_>`_.

License
-------
Copyright 2015 Zalando SE

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

.. _rtd: http://turnstile.readthedocs.org
