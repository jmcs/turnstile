#!/usr/bin/env python
# -*- coding: utf-8 -*-

import git_hooks.models.specifications as specfications


class CommitMessage(object):
    """
    Git commit message
    """

    def __init__(self, message):
        """
        :param message: Commit message
        :type message: str
        """
        self.message = message
        self.specification = specfications.get_specification(message)

    def __str__(self):
        return self.message
