#!/usr/bin/env python
# -*- coding: utf-8 -*-

import abc
import re


class BaseSpecification(object):
    _metaclass__ = abc.ABCMeta

    format = 'Generic Specification'
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
    >>> spec.is_valid()
    True

    >>> spec = JIRASpecification('1000')
    >>> str(spec)
    '1000'
    >>> spec.is_valid()
    False
    """
    TICKET_PATTERN = re.compile('#?(?P<id>[A-Z]+-[0-9]+)')

    format = 'Jira'

    def is_valid(self):
        matches = self.TICKET_PATTERN.match(self._id)
        return bool(matches)


def get_specification(commit_message, specification_format=None):
    """
    Gets the right specification instance for specification_format and commit_message

    >>> s1 = get_specification('something', None)
    >>> type(s1) == Specification
    True

    >>> s2 = get_specification('something', 'jira')
    >>> type(s2) == JIRASpecification
    True

    >>> s3 = get_specification('something', 'invalidstuff')
    Traceback (most recent call last):
        ...
    ValueError: Invalid Specification Type

    :type specification_type:str
    :type commit_message:str
    :return: BaseSpecification
    """
    try:
        specification_id, _ = commit_message.split(' ', 1)
    except ValueError:
        # If there is only one word (the spec) split will fail
        specification_id = commit_message

    try:
        specification_class = _format_class_map[specification_format]
    except KeyError:
        raise ValueError('Invalid Specification Type')
    return specification_class(specification_id)


_format_class_map = {
    None: Specification,  # by default it's a boring Specification without validation
    'jira': JIRASpecification,
}
