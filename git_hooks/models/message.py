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
        # TODO specification objects
        specification_id, _ = message.split(' ', 1)
        self.specification = specfications.Specification(specification_id)

    def __str__(self):
        return self.message
