#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging


def get_logger(command, verbosity='INFO'):
    output = logging.getLogger('githooks-'+command)
    output.setLevel(verbosity)
    output.addHandler(logging.StreamHandler())
    return output
