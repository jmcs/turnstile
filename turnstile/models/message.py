#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Copyright 2015 Zalando SE

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the
License. You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an
"AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific
language governing permissions and limitations under the License.
"""

import turnstile.models.specifications as specfications


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
        self.specification = specfications.get_specification(message)

    def __str__(self):
        return self.message
