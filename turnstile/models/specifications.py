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
import re

import turnstile.common.github as github


class Specification(object):
    def __init__(self, identifier, allowed_formats, allowed_uri_schemes):
        """

        :type identifier: str
        :type allowed_formats: Iterator
        :return:
        """
        self.identifier = identifier
        self.allowed_formats = allowed_formats

        # For URIs
        self.allowed_schemes = allowed_uri_schemes or ['https', 'offline']

    @property
    def format(self):
        """
        Checks the identifier against the allowed formats and returns the first that matches or None if none do.

        :rtype: Optional(str)
        """
        validators = {'github': self.validate_github,
                      'jira': self.validate_jira,
                      'uri': self.validate_uri}

        for format in self.allowed_formats:
            if validators[format]():
                return format

    @property
    def valid(self):
        """
        Goes through all allowed format validators and checks if the identifier is valid in at least one of them

        >>> Specification('https://short.url/spec', {'uri'}, ['https', 'offline']).valid
        True
        >>> Specification('https://10[0]0', {'uri'}, ['https', 'offline']).valid
        False
        >>> Specification('noscheme', {'uri'}, ['https', 'offline']).valid
        False
        >>> Specification('#32', {'uri'}, ['https', 'offline']).valid
        False
        >>> Specification('#32', {'uri', 'github'}, ['https', 'offline']).valid
        True
        """

        return bool(self.format)

    def validate_uri(self):
        """
        Specification URIs have to be valid, have a scheme and be absolute
        :rtype: bool
        """
        uri = rfc3986.uri_reference(self.identifier)
        valid_uri_scheme = uri.scheme in self.allowed_schemes
        return uri.is_valid() and valid_uri_scheme and uri.is_absolute()

    def validate_github(self):
        """
        https://help.github.com/articles/writing-on-github/#references

        :rtype: bool

        >>> Specification('#42', {'github'}, []).validate_github()
        True

        >>> Specification('zalando/turnstile#42', {'github'}, []).validate_github()
        True

        >>> Specification('GH-42', {'github'}, []).validate_github()
        True

        >>> Specification('zalando#42', {'github'}, []).validate_github()
        True

        >>> Specification('32', {'github'}, []).validate_github()
        False
        """
        return bool(github.extract_issue_number(self.identifier))

    def validate_jira(self):
        """
        :rtype: bool

        >>> Specification('CD-42', {'jira'}, []).validate_jira()
        True

        >>> Specification('PROJECT-42', {'jira'}, []).validate_jira()
        True

        >>> Specification('#PROJECT-42', {'jira'}, []).validate_jira()
        True

        >>> Specification('#42', {'jira'}, []).validate_jira()
        False

        >>> Specification('invalid', {'jira'}, []).validate_jira()
        False
        """

        regex = r'#?(?P<id>[A-Z]+-[0-9]+)'
        return bool(re.match(regex, self.identifier))

    def __str__(self):
        return self.identifier


def get_specification(commit_message, allowed_formats, allowed_uri_schemes):
    """
    Extracts the specification URI from the commit_message and creates the appropriate specification instance based on
    the URI scheme. If scheme is missing from the URI the default_specification_format will be used.

    >>> spec = get_specification('something', {'uri'}, {'https'})
    >>> spec.valid
    False

    :type commit_message:str
    :type default_specification_format:str
    :type allowed_uri_schemes: List[str]
    :return: BaseSpecification
    """
    try:
        specification_str, _ = commit_message.split(' ', 1)
    except ValueError:
        # If there is only one word (the spec) split will fail
        specification_str = commit_message

    specification = Specification(specification_str, allowed_formats, allowed_uri_schemes)
    return specification
