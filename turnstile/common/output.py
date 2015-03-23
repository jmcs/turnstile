#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging


def get_root_logger(command):
    output = logging.getLogger('turnstile.'+command)
    output.addHandler(logging.StreamHandler())
    output.setLevel(logging.ERROR)
    return output


def get_sub_logger(parent, name):
    return logging.getLogger('turnstile.{}.{}'.format(parent, name))
