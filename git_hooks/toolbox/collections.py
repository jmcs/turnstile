#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Defines a number of custom collection classes
"""

from __future__ import absolute_import
from collections import Mapping
import copy


class MappingProxy(Mapping):

    """
    An quick-and-dirty immutable variant of `dict`. (Instances aren't truly immutable, of course, since client code can
    mess around with `__source_dict`).
    """

    def __init__(self, source=(), **kwargs):
        self.__source_dict = dict(source, **kwargs)

    def __getitem__(self, key):
        # return a deepcopy to avoid modifying stuff on the original map
        memo = dict()
        return copy.deepcopy(self.__source_dict[key], memo)

    def __setitem__(self, key, value):
        raise TypeError("'{}' object does not support item assignment".format(type(self)))

    def __iter__(self):
        return iter(self.__source_dict)

    def __len__(self):
        return len(self.__source_dict)

    def json_encodable(self):
        return dict(self.__source_dict)
