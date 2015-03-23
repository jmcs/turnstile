[![Build Status](https://travis-ci.org/zalando-bus/turnstile.svg?branch=master)](https://travis-ci.org/zalando-bus/turnstile)
[![Latest Version](https://pypip.in/version/zalando-turnstile/badge.svg)](https://pypi.python.org/pypi/zalando-turnstile)
[![Development Status](https://pypip.in/status/zalando-turnstile/badge.svg)](https://pypi.python.org/pypi/zalando-turnstile)
[![License](https://img.shields.io/pypi/l/zalando-turnstile.svg)](https://github.com/zalando-bus/turnstile/blob/master/LICENSE.txt)
Turnstile - Zalando Local Git Hooks
===================================

Configurable local git hooks.

Installation
------------
You can install turnstile using pip:

    # pip install zalando-turnstile

Alternative you can install it using setup.py

    # setup.py install

Adding and removing turnstile from a repository
-----------------------------------------------
To use turnstile in a repository you have to run `turnstile install` inside the repository.

To remove turnstile from a repository you have to run `turnstile remove` inside the repository.

Configuring turnstile
---------------------
You can configure the global hook behaviour by running `turnstile config`.

Currently you can only configure the hook verbosity.

Repository Configuration
------------------------
To use Turnstile you need to add a configuration file named `.turnstile.yml` to your repository.

You can find an example configuration in [turnstile repository](.turnstile.yml) and you can read can learn more about
the configuration options in the [documentation](docs/user/configuration.md).
