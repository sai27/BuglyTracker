#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Default configurations.
'''

__author__ = 'sai27'

configs = {
    'debug': True,
    'host':'127.0.0.1',
    'port':8000,
    'db': {
        'host': '127.0.0.1',
        'port': 3306,
        'user': 'root',
        'password': '123456',
        'db': 'bugly'
    },
    'session': {
        'secret': 'bugly'
    },
    'page' : 20
}