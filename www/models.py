#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'sai27'

import time, uuid

from orm import Model, StringField, BooleanField, FloatField, TextField, IntegerField

def next_id():
    return '%015d%s000' % (int(time.time() * 1000), uuid.uuid4().hex)

class User(Model):
    __table__ = 'users'

    id          = StringField(primary_key=True, default=next_id, ddl='varchar(50)')
    email       = StringField(ddl='varchar(50)')
    passwd      = StringField(ddl='varchar(50)')
    admin       = BooleanField()
    name        = StringField(ddl='varchar(50)')
    created_at  = FloatField(default=time.time)

class Issue(Model):
    __table__ = 'issues'

    id          = IntegerField(primary_key=True)
    title       = StringField(ddl='varchar(256)')
    content     = TextField()
    content_md5 = StringField(ddl='varchar(50)')
    version     = StringField(ddl='varchar(32)')
    user_id     = StringField(ddl='varchar(50)')
    status      = IntegerField()
    
class Crash(Model):
    __table__ = 'crashs'

    id          = StringField(primary_key=True, ddl='varchar(50)')
    issue_id    = StringField(ddl='varchar(50)')
    crash_doc   = TextField()
    app_detail  = TextField()

