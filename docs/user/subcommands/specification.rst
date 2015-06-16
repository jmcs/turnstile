.. _specification_command:

specification
=============

This subcommand verifies if the commit messages in a range of revisions have valid specifications.

This command takes the same revision ranges as ``git log`` to specify the revision ranges.

When using the verbose mode merge commits are printed otherwise they are simply ignored.

Usage
-----

::

    $ turnstile specification [<revision range>]
