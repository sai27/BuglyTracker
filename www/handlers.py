#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' url handlers '

__author__ = 'sai27'

import re, time, json, logging, hashlib, base64, asyncio

#import markdown2

from aiohttp import web

from coroweb import get, post
from apis import Page, APIValueError, APIResourceNotFoundError

from models import User, Comment, Blog, next_id
from config import configs

COOKIE_NAME = 'awesession'
_COOKIE_KEY = configs.session.secret

def check_admin(request):
    if request.__user__ is None or not request.__user__.admin:
        raise APIPermissionError()

def get_page_index(page_str):
    p = 1
    try:
        p = int(page_str)
    except ValueError as e:
        pass
    if p < 1:
        p = 1
    return p
    
def user2cookie(user, max_age):
    '''
    Generate cookie str by user.
    '''
    # build cookie string by: id-expires-sha1
    expires = str(int(time.time() + max_age))
    s = '%s-%s-%s-%s' % (user.id, user.passwd, expires, _COOKIE_KEY)
    L = [user.id, expires, hashlib.sha1(s.encode('utf-8')).hexdigest()]
    return '-'.join(L)

async def cookie2user(cookie_str):
    '''
    Parse cookie and load user if cookie is valid.
    '''
    if not cookie_str:
        return None
    try:
        L = cookie_str.split('-')
        if len(L) != 3:
            return None
        uid, expires, sha1 = L
        if int(expires) < time.time():
            return None
        user = await User.find(uid)
        if user is None:
            return None
        s = '%s-%s-%s-%s' % (uid, user.passwd, expires, _COOKIE_KEY)
        if sha1 != hashlib.sha1(s.encode('utf-8')).hexdigest():
            logging.info('invalid sha1')
            return None
        user.passwd = '******'
        return user
    except Exception as e:
        logging.exception(e)
        return None
        
@get('/')
async def index(*, page='1'):
    '''page_index = get_page_index(page)
    num = await Blog.findNumber('count(id)')
    page = Page(num)
    if num == 0:
        blogs = []
    else:
        print(page)
        blogs = await Blog.findAll(orderBy='created_at desc', limit=(page.offset, page.limit))'''
    print('page:',page)
    return {
        '__template__': 'issues.html',
        'pages': 50,
        'cur_page':int(page),
        'issues': [
            { 'id' : 10001, 'text' : 'failed call lua function : [string \"gui/supermarket/ui_sub_activity_hy.bytes\"]:316: attempt to index a nil value', 'version' : '2.6.20170203', 'user_name' : '于静波', 'status' : '处理中' },
            { 'id' : 10002, 'text' : 'PCall failed : [string \"game/data/lua_data_ach.bytes\"]:533: attempt to index a nil value', 'version' : '2.6.20170203', 'user_name' : '于静波', 'status' : '已解决' },
            { 'id' : 10003, 'text' : 'PCall failed : [string \"game/data/lua_data_ach.bytes\"]:533: attempt to index a nil value', 'version' : '2.6.20170203', 'user_name' : '无', 'status' : '未处理' },
            { 'id' : 10003, 'text' : 'PCall failed : [string \"game/data/lua_data_ach.bytes\"]:533: attempt to index a nil value', 'version' : '2.6.20170203', 'user_name' : '无', 'status' : '未处理' },
            { 'id' : 10003, 'text' : 'PCall failed : [string \"game/data/lua_data_ach.bytes\"]:533: attempt to index a nil value', 'version' : '2.6.20170203', 'user_name' : '无', 'status' : '未处理' },
            { 'id' : 10003, 'text' : 'PCall failed : [string \"game/data/lua_data_ach.bytes\"]:533: attempt to index a nil value', 'version' : '2.6.20170203', 'user_name' : '无', 'status' : '未处理' },
            { 'id' : 10003, 'text' : 'PCall failed : [string \"game/data/lua_data_ach.bytes\"]:533: attempt to index a nil value', 'version' : '2.6.20170203', 'user_name' : '无', 'status' : '未处理' },
            { 'id' : 10003, 'text' : 'PCall failed : [string \"game/data/lua_data_ach.bytes\"]:533: attempt to index a nil value', 'version' : '2.6.20170203', 'user_name' : '无', 'status' : '未处理' },
            { 'id' : 10003, 'text' : 'PCall failed : [string \"game/data/lua_data_ach.bytes\"]:533: attempt to index a nil value', 'version' : '2.6.20170203', 'user_name' : '无', 'status' : '未处理' },
            { 'id' : 10003, 'text' : 'PCall failed : [string \"game/data/lua_data_ach.bytes\"]:533: attempt to index a nil value', 'version' : '2.6.20170203', 'user_name' : '无', 'status' : '未处理' },
            { 'id' : 10003, 'text' : 'PCall failed : [string \"game/data/lua_data_ach.bytes\"]:533: attempt to index a nil value', 'version' : '2.6.20170203', 'user_name' : '无', 'status' : '未处理' },
            { 'id' : 10003, 'text' : 'PCall failed : [string \"game/data/lua_data_ach.bytes\"]:533: attempt to index a nil value', 'version' : '2.6.20170203', 'user_name' : '无', 'status' : '未处理' },
            { 'id' : 10003, 'text' : 'PCall failed : [string \"game/data/lua_data_ach.bytes\"]:533: attempt to index a nil value', 'version' : '2.6.20170203', 'user_name' : '无', 'status' : '未处理' },
            { 'id' : 10003, 'text' : 'PCall failed : [string \"game/data/lua_data_ach.bytes\"]:533: attempt to index a nil value', 'version' : '2.6.20170203', 'user_name' : '无', 'status' : '未处理' },
            { 'id' : 10003, 'text' : 'PCall failed : [string \"game/data/lua_data_ach.bytes\"]:533: attempt to index a nil value', 'version' : '2.6.20170203', 'user_name' : '无', 'status' : '未处理' },
            { 'id' : 10003, 'text' : 'PCall failed : [string \"game/data/lua_data_ach.bytes\"]:533: attempt to index a nil value', 'version' : '2.6.20170203', 'user_name' : '无', 'status' : '未处理' },
            { 'id' : 10003, 'text' : 'PCall failed : [string \"game/data/lua_data_ach.bytes\"]:533: attempt to index a nil value', 'version' : '2.6.20170203', 'user_name' : '无', 'status' : '未处理' },
            { 'id' : 10003, 'text' : 'PCall failed : [string \"game/data/lua_data_ach.bytes\"]:533: attempt to index a nil value', 'version' : '2.6.20170203', 'user_name' : '无', 'status' : '未处理' },
            { 'id' : 10003, 'text' : 'PCall failed : [string \"game/data/lua_data_ach.bytes\"]:533: attempt to index a nil value', 'version' : '2.6.20170203', 'user_name' : '无', 'status' : '未处理' },
            { 'id' : 10003, 'text' : 'PCall failed : [string \"game/data/lua_data_ach.bytes\"]:533: attempt to index a nil value', 'version' : '2.6.20170203', 'user_name' : '无', 'status' : '未处理' }
        ]
    }
    
@get('/claim')
async def claim(*, page='1'):
    return {
        '__template__': 'issues.html',
        'pages': 50,
        'cur_page':int(page),
        'issues': [
            { 'id' : 10011, 'text' : 'PCall failed : [string \"game/data/lua_data_ach.bytes\"]:533: attempt to index a nil value', 'version' : '2.6.20170203', 'user_name' : '无', 'status' : '未处理' },
            { 'id' : 10012, 'text' : 'PCall failed : [string \"game/data/lua_data_ach.bytes\"]:533: attempt to index a nil value', 'version' : '2.6.20170203', 'user_name' : '无', 'status' : '未处理' },
            { 'id' : 10013, 'text' : 'PCall failed : [string \"game/data/lua_data_ach.bytes\"]:533: attempt to index a nil value', 'version' : '2.6.20170203', 'user_name' : '无', 'status' : '未处理' }
        ]
    }
    
@get('/my')
async def my(*, page='1'):
    return {
        '__template__': 'issues.html',
        'pages': 50,
        'cur_page':int(page),
        'issues': [
            { 'id' : 10021, 'text' : 'PCall failed : [string \"game/data/lua_data_ach.bytes\"]:533: attempt to index a nil value', 'version' : '2.6.20170203', 'user_name' : '于静波', 'status' : '处理中' },
            { 'id' : 10022, 'text' : 'PCall failed : [string \"game/data/lua_data_ach.bytes\"]:533: attempt to index a nil value', 'version' : '2.6.20170203', 'user_name' : '于静波', 'status' : '处理中' },
            { 'id' : 10023, 'text' : 'PCall failed : [string \"game/data/lua_data_ach.bytes\"]:533: attempt to index a nil value', 'version' : '2.6.20170203', 'user_name' : '于静波', 'status' : '处理中' }
        ]
    }

@get('/issue/{id}')
async def issue(id):
    return {
        '__template__': 'issue_detail.html',
        'id':100001,
        'text':'''"failed call lua function : [string "gui/supermarket/ui_sub_activity_hy.bytes"]:316: attempt to index a nil value
stack traceback:
	[string "gui/supermarket/ui_sub_activity_hy.bytes"]:316: in function 'SetItemInfo'
	[string "gui/supermarket/ui_sub_activity_hy.bytes"]:457: in function 'RefreshUI'
	[string "gui/supermarket/ui_sub_activity_hy.bytes"]:895: in function 'callback'
	[string "libs/sig/lua_sig.bytes"]:35: in function 'fn'
	[string "libs/sig/lua_sig.bytes"]:169: in function 'InvokePerson'
	[string "game/data/lua_data_ach.bytes"]:410: in function 'SetAchieve'
	[string "game/data/lua_data_notify.bytes"]:188: in function 'callback'
	[string "libs/net/lua_net.bytes"]:55: in function <[string "libs/net/lua_net.bytes"]:51>"''',
        'version' : '2.6.20170203', 
        'user_name' : '于静波', 
        'status' : '处理中',
        'devices' : [
            '00_20_5D_9D_BE_12_72_12_CA_32_CD_8F_8E_85_11_16',
            '00_20_5D_9D_BE_12_72_12_CA_32_CD_8F_8E_85_11_17',
            '00_20_5D_9D_BE_12_72_12_CA_32_CD_8F_8E_85_11_18',
            '00_20_5D_9D_BE_12_72_12_CA_32_CD_8F_8E_85_11_19',
            '00_20_5D_9D_BE_12_72_12_CA_32_CD_8F_8E_85_11_20',
        ]
    }
    
@get('/register')
def register():
    return {
        '__template__': 'register.html'
    }

@get('/signin')
def signin():
    return {
        '__template__': 'signin.html'
    }

@get('/signout')
def signout(request):
    referer = request.headers.get('Referer')
    r = web.HTTPFound(referer or '/')
    r.set_cookie(COOKIE_NAME, '-deleted-', max_age=0, httponly=True)
    logging.info('user signed out.')
    return r
    
@post('/api/authenticate')
async def authenticate(*, email, passwd):
    if not email:
        raise APIValueError('email', 'Invalid email.')
    if not passwd:
        raise APIValueError('passwd', 'Invalid password.')
    users = await User.findAll('email=?', [email])
    if len(users) == 0:
        raise APIValueError('email', 'Email not exist.')
    user = users[0]
    # check passwd:
    sha1 = hashlib.sha1()
    sha1.update(user.id.encode('utf-8'))
    sha1.update(b':')
    sha1.update(passwd.encode('utf-8'))
    if user.passwd != sha1.hexdigest():
        raise APIValueError('passwd', 'Invalid password.')
    # authenticate ok, set cookie:
    r = web.Response()
    r.set_cookie(COOKIE_NAME, user2cookie(user, 86400), max_age=86400, httponly=True)
    user.passwd = '******'
    r.content_type = 'application/json'
    r.body = json.dumps(user, ensure_ascii=False).encode('utf-8')
    return r

_RE_EMAIL = re.compile(r'^[a-z0-9\.\-\_]+\@[a-z0-9\-\_]+(\.[a-z0-9\-\_]+){1,4}$')
_RE_SHA1 = re.compile(r'^[0-9a-f]{40}$')

@post('/api/users')
async def api_register_user(*, email, name, passwd):
    if not name or not name.strip():
        raise APIValueError('name')
    if not email or not _RE_EMAIL.match(email):
        raise APIValueError('email')
    if not passwd or not _RE_SHA1.match(passwd):
        raise APIValueError('passwd')
    users = await User.findAll('email=?', [email])
    if len(users) > 0:
        raise APIError('register:failed', 'email', 'Email is already in use.')
    uid = next_id()
    sha1_passwd = '%s:%s' % (uid, passwd)
    user = User(id=uid, name=name.strip(), email=email, passwd=hashlib.sha1(sha1_passwd.encode('utf-8')).hexdigest(), image='http://www.gravatar.com/avatar/%s?d=mm&s=120' % hashlib.md5(email.encode('utf-8')).hexdigest())
    await user.save()
    # make session cookie:
    r = web.Response()
    r.set_cookie(COOKIE_NAME, user2cookie(user, 86400), max_age=86400, httponly=True)
    user.passwd = '******'
    r.content_type = 'application/json'
    r.body = json.dumps(user, ensure_ascii=False).encode('utf-8')
    return r