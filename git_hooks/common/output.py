#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging


def get_logger(command):
    output = logging.getLogger('githooks-'+command)
    output.addHandler(logging.StreamHandler())
    output.setLevel(logging.ERROR)
    return output
