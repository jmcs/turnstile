#!/usr/bin/env python
# -*- coding: utf-8 -*-

import abc
import re


class BaseSpecification(object):
    _metaclass__ = abc.ABCMeta

    format = 'Generic Specification'

    @property
    @abc.abstractmethod
    def id(self):
        """
        Specification ID. This is a method to be able to ensure it exists
        :rtype: str
        """

    @abc.abstractmethod
    def is_valid(self):
        """
        Whether a specification id is valid or not
        :rtype: bool
        """

    def __str__(self):
        return self.id


class Specification(BaseSpecification):
    """
    Boring meaningless Specification

    >>> spec = Specification('CD-1000')
    >>> str(spec)
    'CD-1000'
    >>> spec.is_valid()
    True

    >>> spec = Specification('1000')
    >>> str(spec)
    '1000'
    >>> spec.is_valid()
    True
    """
    def __init__(self, specification_id):
        self._id = specification_id

    @property
    def id(self):
        return self._id

    def is_valid(self):
        """
        A generic specification is always valid
        :rtype: bool
        """
        return True


class JIRASpecification(Specification):
    """
    Jira ticket as specification

    >>> spec = JIRASpecification('CD-1000')
    >>> str(spec)
    'CD-1000'

    >>> spec = JIRASpecification('1000')
    >>> str(spec)
    '1000'
    """
    TICKET_PATTERN = re.compile('#?(?P<id>[A-Z]+-[0-9]+)')

    format = 'Jira'

    @property
    def project(self):
        """
        >>> JIRASpecification('CD-1000').project
        'CD'
        >>> JIRASpecification('PF-20').project
        'PF'
        >>> JIRASpecification('#PF-20').project
        'PF'
        >>> JIRASpecification('IDontEvenKnowWhatThisIs').project
        ''

        :return: Ticket Project (e.g. CD-1000 -> CD)
        :rtype: str
        """
        if self.is_valid():
            project, ticket_number = self._id.split('-', 1)
            return project.lstrip('#')  # if spec id starts with # that is not part of the project
        else:
            return ''

    def is_valid(self):
        """
        >>> JIRASpecification('CD-1000').is_valid()
        True
        >>> JIRASpecification('PF-1000').is_valid()
        True
        >>> JIRASpecification('JIRA-1000').is_valid()
        True
        >>> JIRASpecification('PROJECT').is_valid()
        False
        >>> JIRASpecification('lower-1000').is_valid()
        False
        >>> JIRASpecification('1000').is_valid()
        False
        >>> JIRASpecification("dön't bréãk plèâs€").is_valid()
        False
        """
        matches = self.TICKET_PATTERN.match(self._id)
        return bool(matches)


class GithubSpecification(Specification):
    """
    Github issue as specification

    >>> spec = GithubSpecification('CD-1000')
    >>> str(spec)
    'CD-1000'

    >>> spec = GithubSpecification('1000')
    >>> str(spec)
    '1000'
    """
    format = 'Github'

    def is_valid(self):
        """
        >>> GithubSpecification('1000').is_valid()
        True
        >>> GithubSpecification('PF-1000').is_valid()
        False
        >>> GithubSpecification('1.1').is_valid()
        False
        """
        return self._id.isdigit()


def get_specification(commit_message, default_specification_format=None):
    """
    Extracts the specification URI from the commit_message and creates the appropriate specification instance based on
    the URI scheme. If scheme is missing from the URI the default_specification_format will be used.

    >>> spec = get_specification('something', None)
    >>> type(spec) == Specification
    True

    >>> spec = get_specification('something', 'jira')
    >>> type(spec) == JIRASpecification
    True

    >>> spec = get_specification('jira:something', None)
    >>> type(spec) == JIRASpecification
    True

    >>> spec = get_specification('#github:something')
    >>> type(spec) == GithubSpecification
    True

    >>> spec = get_specification('something', 'invalidstuff')
    Traceback (most recent call last):
        ...
    ValueError: Invalid Specification Type

    :type commit_message:str
    :type default_specification_format:str
    :return: BaseSpecification
    """
    try:
        specification_uri, _ = commit_message.split(' ', 1)
    except ValueError:
        # If there is only one word (the spec) split will fail
        specification_uri = commit_message

    specification_uri = specification_uri.lstrip('#')  # remove the initial # from the specification

    if ':' in specification_uri:
        specification_scheme, specification_path = specification_uri.split(':', 1)
    else:
        specification_scheme = default_specification_format if default_specification_format else 'generic'
        specification_path = specification_uri

    try:
        specification_class = _format_class_map[specification_scheme]
    except KeyError:
        raise ValueError('Invalid Specification Type')
    return specification_class(specification_path)


_format_class_map = {
    'generic': Specification,  # by default it's a boring Specification without validation
    'jira': JIRASpecification,
    'github': GithubSpecification,
}
