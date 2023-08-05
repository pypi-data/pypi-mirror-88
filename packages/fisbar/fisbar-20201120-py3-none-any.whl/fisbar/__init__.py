#!/usr/env python
# -*- coding: utf-8 -*-
# -*- format: python -*-
# -*- author: G. Henning -*-
# -*- created: november 2020 -*-
# -*- copyright: GH/IPHC 2020 -*-
# -*- file: init -*-
# -*- purpose: -*-

'''
Module: fisbar

A python implementation of A. Sierk's fisbar fortran routine.

'''
import warnings
import sys


if sys.version_info < (3, 6):
    warnings.warn("# WARNING: faster module has been designed for python 3.6 and higher")
elif sys.version_info <= (3, 5):
    raise RuntimeError("Module should be used with python 3.6 or higher")


from .fisbar import fisbar

# EOF
