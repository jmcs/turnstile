#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Defines a number of custom collection classes

Copyright 2015 Zalando SE

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the
License. You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an
"AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific
language governing permissions and limitations under the License.
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
