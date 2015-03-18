#!/usr/bin/env python
# -*- coding: utf-8 -*-

import git_hooks.models.specifications as specfications


class CommitMessage(object):
    """
    Git commit message
    """

    def __init__(self, message, specification_type):
        """
        :param message: Commit message
        :type message: str
        :type specification_type: str
        """
        self.message = message.strip()
        self.specification = specfications.get_specification(message, specification_type)

    def __str__(self):
        return self.message
