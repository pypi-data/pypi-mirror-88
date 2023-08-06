#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time           : 20-4-27 下午3:05
# @Author         : Shen Bin
# @File           : rest.py
# @Product        : PyCharm
# @Docs           :
# @Source         :

import requests

from aicloud.cloudexception import CommonError


class Object(dict):
    def __init__(self, init_dict=None, deep=False):
        super(Object, self).__init__()

        if isinstance(init_dict, dict):
            for k, v in init_dict.items():
                if deep:
                    if isinstance(v, dict):
                        if not isinstance(v, Object):
                            v = Object(v, deep)
                    elif isinstance(v, (list, tuple)):
                        v = [Object(i, deep) if (isinstance(i, dict) and not isinstance(i, Object)) else i for i in v]
                setattr(self, k, v)
                self[k] = v

    def __getattr__(self, key):
        pass

    def __getitem__(self, key):
        return getattr(self, key)


def _resp(r, no_error):
    if no_error and r.status_code >= 400:
        raise CommonError(code=r.status_code, message=r.content)

    return r.status_code, r.headers, r


def _resp_content(r):
    body = ""
    try:
        if r.text:
            body = r.json()
    except:
        raise CommonError(code=r.status_code, message=r.text)

    return r.status_code, r.headers, Object(body, True), r.content


def head(url, headers={}, verify=False, no_error=False, hooks=None):
    r = requests.get(url, headers=headers, verify=verify, hooks=hooks)
    return _resp(r, no_error)


def get(url, headers={}, verify=False, no_error=False, params=None, hooks=None):
    r = requests.get(url, headers=headers, verify=verify, params=params, hooks=hooks)
    return _resp(r, no_error)


def post(url, headers={}, body=None, verify=False, no_error=False, data=None, files=None, hooks=None):
    r = requests.post(url, headers=headers, json=body, data=data, verify=verify, files=files, hooks=hooks)
    return _resp(r, no_error)


def post_timeout(url, headers={}, body=None, verify=False, no_error=False, hooks=None):
    r = requests.post(url, headers=headers, json=body, verify=verify, timeout=8, hooks=hooks)
    return _resp(r, no_error)


def put(url, headers={}, body=None, verify=False, no_error=False, params=None, data=None, hooks=None):
    r = requests.put(url, headers=headers, json=body, params=params, data=data, verify=verify, hooks=hooks)
    return _resp(r, no_error)


def patch(url, headers={}, body=None, verify=False, no_error=False, hooks=None):
    r = requests.patch(url, headers=headers, json=body, verify=verify, hooks=hooks)
    return _resp(r, no_error)


def delete(url, headers={}, verify=False, no_error=False, hooks=None):
    r = requests.delete(url, headers=headers, verify=verify, hooks=hooks)
    return _resp(r, no_error)
