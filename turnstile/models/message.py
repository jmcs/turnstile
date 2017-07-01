#!/usr/bin/env python
# -*- coding: utf-8 -*-


class CommitMessage(object):
    """
    Git commit message

    >>> commit_message = CommitMessage('branch', 'test message')
    >>> str(commit_message)
    'test message'
    """

    def __init__(self, branch, message):
        """
        :param branch: Active branch
        :type branch: str
        :param message: Commit message
        :type message: str
        """
        self.branch = branch
        self.message = message.strip()

    def __str__(self):
        return self.message
