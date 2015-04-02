#!/usr/bin/env python
# -*- coding: utf-8 -*-

import turnstile.models.specifications as specfications


class CommitMessage(object):
    """
    Git commit message
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
        self.specification = specfications.get_specification(message)

    def __str__(self):
        return self.message
