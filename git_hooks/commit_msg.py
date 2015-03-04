#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

from click import command, argument


@command()
@argument('message_file')
def commit_msg(message_file):
    """
    This hook is invoked by git commit, and can be bypassed with --no-verify option. It takes a single parameter,
    the name of the file that holds the proposed commit log message.
    Exiting with non-zero status causes the git commit to abort.

    :param message_file: the name of the file that holds the proposed commit log message
    :type message_file: string
    """

    print('commit-msg hook')
    print(message_file)

if __name__ == '__main__':
    commit_msg()
