#!/usr/bin/env python
# -*- coding: utf-8 -*-

import abc


class BaseSpecification(object):
    _metaclass__ = abc.ABCMeta

    @property
    @abc.abstractmethod
    def id(self):
        """
        Specification ID. This is a method to be able to ensure it exists
        :rtype: str
        """
        pass

    @abc.abstractmethod
    def is_valid(self):
        """
        Whether a specification id is valid or not
        :rtype: bool
        """
        pass

    def __str__(self):
        return self.id


class Specification(BaseSpecification):
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
