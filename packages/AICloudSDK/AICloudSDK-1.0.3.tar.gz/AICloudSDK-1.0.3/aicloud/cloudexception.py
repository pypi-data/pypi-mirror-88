#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time           : 20-4-27 下午2:54
# @Author         : Shen Bin
# @File           : cloudexception.py
# @Product        : PyCharm
# @Docs           :
# @Source         :


class CommonError(Exception):
    code = 500
    error = "CommonError"
    message = "unknown error."

    def __init__(self, code=None, error=None, message=None):
        self.code = self.__class__.code if not code else code
        self.error = self.__class__.error if not error else error
        self.message = self.__class__.message if not message else message

    def __str__(self):
        return '<{}>: {}'.format(self.__class__.__name__, self.message)
