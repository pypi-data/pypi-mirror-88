#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: 深圳星河软通科技有限公司 A.Star
# @contact: astar@snowland.ltd
# @site: www.astar.ltd
# @file: _base .py
# @time: 2020/6/19 1:26
# @Software: PyCharm

__all__ = [
    'BaseClient'
]

from snowland_authsdk.login import Account


class BaseClient(Account):
    def __init__(self, url, username='admin', password='admin'):
        self.url = url
        if url[-1] != '/':
            self.url += '/'
        super(BaseClient, self).__init__(username, password)

    @property
    def username(self):
        return self.access_key

    @property
    def password(self):
        return self.access_secret
