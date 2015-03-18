#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging


def get_root_logger(command):
    output = logging.getLogger('git-hook.'+command)
    output.addHandler(logging.StreamHandler())
    output.setLevel(logging.ERROR)
    return output


def get_sub_logger(parent, name):
    return logging.getLogger('git-hook.{}.{}'.format(parent, name))
