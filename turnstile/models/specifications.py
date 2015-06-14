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

import rfc3986


class Specification(object):

    def __init__(self, uri):
        self.uri = rfc3986.uri_reference(uri)
        self.scheme = self.uri.scheme

    @property
    def valid(self):
        """
        Specification URIs have to be valid, have a scheme and be absolute
        >>> Specification('https://short.url/spec').valid
        True
        >>> Specification('https://10[0]0').valid
        False
        >>> Specification('noscheme').valid
        False
        """
        return bool(self.uri.is_valid() and self.scheme and self.uri.is_absolute())

    def __str__(self):
        return self.uri.unsplit()


def get_specification(commit_message):
    """
    Extracts the specification URI from the commit_message and creates the appropriate specification instance based on
    the URI scheme. If scheme is missing from the URI the default_specification_format will be used.

    >>> spec = get_specification('something')
    >>> spec.valid
    False

    >>> spec = get_specification('http://spec.url')
    >>> spec.scheme
    u'http'

    >>> spec = get_specification('https://spec.url')
    >>> spec.scheme
    u'https'

    :type commit_message:str
    :type default_specification_format:str
    :return: BaseSpecification
    """
    try:
        specification_str, _ = commit_message.split(' ', 1)
    except ValueError:
        # If there is only one word (the spec) split will fail
        specification_str = commit_message

    specification = Specification(specification_str)
    return specification
