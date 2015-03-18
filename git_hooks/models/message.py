#!/usr/bin/env python
# -*- coding: utf-8 -*-

import git_hooks.models.specifications as specfications


class CommitMessage(object):
    """
    Git commit message
    """

    def __init__(self, message, specification_format):
        """
        :param message: Commit message
        :type message: str
        :type specification_format: str
        """
        self.message = message.strip()
        self.specification = specfications.get_specification(message, specification_format)

    def __str__(self):
        return self.message
