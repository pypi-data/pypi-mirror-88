#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: 深圳星河软通科技有限公司 A.Star
# @contact: astar@snowland.ltd
# @site: www.astar.ltd
# @file: __init__.py .py
# @time: 2020/6/15 22:33
# @Software: PyCharm

from astartool.setuptool import get_version


VERSION = (0, 0, 3, 'final', 0)
__version__ = get_version(VERSION)

del get_version
