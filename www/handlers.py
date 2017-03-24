#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' url handlers '

__author__ = 'sai27'

import re, time, json, logging, hashlib, base64, asyncio

import orm
#import markdown2

from aiohttp import web

from coroweb import get, post
from apis import APIValueError, APIResourceNotFoundError

from models import User, Issue, Crash, next_id
from config import configs

COOKIE_NAME = 'buglytracker_session'
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
    users = await User.findAll()
    count = await Issue.findNumber('count(id)')
    cur_page = get_page_index(page)
    pages = count // configs.page + 1
    
    items = await Issue.findAll( limit=((cur_page-1)*configs.page, configs.page))
    issues = list()
    for item in items:
        sql = r"SELECT COUNT(*) _num_ FROM crashs WHERE issue_id = %s"
        count = await orm.select(sql, [item.id])
        issue = dict()
        issue['id']         = item.id
        issue['text']       = item.title
        issue['version']    = item.version
        issue['count']      = count[0]['_num_']
        if item.user_id == None:
            issue['user_name']  = "无"
            issue['status']     = "未处理"
        else:
            name = '无'
            for user in users:
                if user.id == item.user_id:
                    name = user.name
                    break  
            issue['user_name']  = name
            if item.status == 0:
                issue['status']     = "处理中"
            elif item.status == 1:
                issue['status']     = "已解决"
        issues.append(issue)
        
    return {
        '__template__': 'issues.html',
        'pages': pages,
        'cur_page':cur_page,
        'issues': issues
    }
    
@get('/claim')
async def claim(*, page='1'):
    users = await User.findAll()
    count = await Issue.findNumber('count(id)', where='user_id IS NULL')
    cur_page = get_page_index(page)
    pages = count // configs.page + 1
    
    items = await Issue.findAll(where = 'user_id IS NULL', limit=((cur_page-1)*configs.page, configs.page) )
    issues = list()
    for item in items:
        sql = r"SELECT COUNT(*) _num_ FROM crashs WHERE issue_id = %s"
        count = await orm.select(sql, [item.id])
        issue = dict()
        issue['id']         = item.id
        issue['text']       = item.title
        issue['version']    = item.version
        issue['count']      = count[0]['_num_']
        issue['user_name']  = "无"
        issue['status']     = "未处理"
        issues.append(issue)
        
    return {
        '__template__': 'issues.html',
        'pages': pages,
        'cur_page':cur_page,
        'issues': issues
    }
    
@get('/my')
async def my(request, *, page='1'):
    users = await User.findAll()
    count = await Issue.findNumber('count(id)', where=r"`user_id` = '%s'"%request.__user__.id )
    cur_page = get_page_index(page)
    pages = count // configs.page + 1
    
    items = await Issue.findAll(where = r"`user_id` = '%s'"%(request.__user__.id), limit=((cur_page-1)*configs.page, configs.page) )
    issues = list()
    for item in items:
        sql = r"SELECT COUNT(*) _num_ FROM crashs WHERE issue_id = %s"
        count = await orm.select(sql, [item.id])
        issue = dict()
        issue['id']         = item.id
        issue['text']       = item.title
        issue['version']    = item.version
        issue['count']      = count[0]['_num_']
        issue['user_name']  = request.__user__.name
        if item.status == 0:
            issue['status']     = "处理中"
        elif item.status == 1:
            issue['status']     = "已解决"
        issues.append(issue)
        
    return {
        '__template__': 'issues.html',
        'pages': pages,
        'cur_page':cur_page,
        'issues': issues
    }

@get('/issue/{id}')
async def issue(request, *, id):
    users = await User.findAll()
    issue = await Issue.find(id)
    
    if issue.user_id == None:
        user_name   = "无"
        status      = "未处理"
        if request.__user__ == None:
            handle_type = 3
        else:
            handle_type = 0
    else:
        if request.__user__ == None or issue.user_id != request.__user__.id:
            user_name = '无'
            handle_type = 3
            if issue.status == 0:
                status = "处理中"
            elif issue.status == 1:
                status = "已解决"
            for user in users:
                if user.id == issue.user_id:
                    user_name = user.name
                    break  
        else:
            user_name = request.__user__.name
            if issue.status == 0:
                status = "处理中"
                handle_type = 1
            elif issue.status == 1:
                status = "已解决"
                handle_type = 2
    
    sql = r"SELECT COUNT(*) _num_ FROM crashs WHERE issue_id = %s"
    count = await orm.select(sql, [id])
    #print(count)
    sql = r"SELECT id FROM crashs WHERE issue_id = %s limit 5"
    crashs = await orm.select(sql, [id])
    #crashs = await Crash.findAll(where = 'issue_id = %s'%id)
    devices = []
    #print(crashs)
    for crash in crashs:
        devices.append(crash['id'])
        
    return {
        '__template__': 'issue_detail.html',
        'id':issue.id,
        'text':issue.content,
        'version' : issue.version,
        'user_name' : user_name,
        'status' : status,
        'handle_type' : handle_type,
        'devices' : devices,
        'count' : count[0]['_num_']
    }
    
@get('/api/crashdoc/{id}')
async def crashdoc(*, id):
    id = id[:-14]
    print(id)
    crash = await Crash.find(id)
    if crash == None:
        raise APIValueError('crash_id', '没有找到对应crash文件')
        
    bytes = crash.crash_doc.encode('utf-8')
    print ('bytes', type(bytes))
    return bytes
    
@get('/api/appdetail/{id}')
async def appdetail(*, id):
    id = id[:-15]
    crash = await Crash.find(id)
    if crash == None:
        raise APIValueError('crash_id', '没有找到对应crash文件')
        
    bytes = crash.app_detail.encode('utf-8')
    print ('bytes', type(bytes))
    return bytes
    
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
    user = User(id=uid, name=name.strip(), email=email, passwd=hashlib.sha1(sha1_passwd.encode('utf-8')).hexdigest())
    await user.save()
    # make session cookie:
    r = web.Response()
    r.set_cookie(COOKIE_NAME, user2cookie(user, 86400), max_age=86400, httponly=True)
    user.passwd = '******'
    r.content_type = 'application/json'
    r.body = json.dumps(user, ensure_ascii=False).encode('utf-8')
    return r
    
@post('/api/issue_op')
async def api_issue_op(request, *, issue_id, op):
    if op == None:
        raise APIValueError('op', 'op为空')
    
    if not isinstance(op, int):
        raise APIValueError('op', '找不到状态信息')
        
    if not request.__user__:
        raise APIValueError('op', '请先登录')
        
    issue = await Issue.find(issue_id)
    
    print(type(issue))
    if not issue:
        raise APIValueError('op', '找不到issue')
        
    # 领取
    if op == 0:
        if issue.user_id == None:
            issue.user_id = request.__user__.id
            issue.status = 0
            await issue.update()
        else:
            raise APIValueError('op', 'issue状态有变化，请刷新页面')
    # 解决
    elif op == 1:
        if issue.user_id == request.__user__.id:
            issue.status = 1
            await issue.update()
    # 放弃
    elif op == 2:
        if issue.user_id == request.__user__.id:
            issue.user_id = None
            issue.status = 0
            await issue.update()
    # 重开
    elif op == 3:
        if issue.user_id == request.__user__.id:
            issue.status = 0
            await issue.update()
    
    return { 'status' : 200 }
 
@post('/api/upload')
async def api_upload(*, name, crashDoc, appDetail):
    crash = await Crash.find(name)
    if crash:
        raise APIValueError('upload', '重复导入:%s'%name)
        
    jsonCrashDoc = json.loads(crashDoc)
    crashMap = jsonCrashDoc.get('crashMap',None)
    if not crashMap:
        raise APIValueError('upload', '找不到crashMap:%s'%name)
    
    version = crashMap.get('productVersion',None)
    if not version:
        raise APIValueError('upload', '找不到productVersion:%s'%name)
        
    content = crashMap.get('expMessage',None)
    if not content:
        raise APIValueError('upload', '找不到expMessage:%s'%name)
        
    content = content.replace('\\"', '\"')
    content = content.replace('\\n', '\n')
    content = content.replace('\\t', '\t')
    content_md5 = hashlib.md5(content.encode('utf-8')).hexdigest()
    length = content.find('\n')
    if length >= 0:
        title = content[:length]
    else:
        title = content[:]
        
    issues = await Issue.findAll(where=r"`content_md5` = '%s' AND `version` = '%s'"%(content_md5, version))
    if (len(issues) == 1):
        issue_id = issues[0].id
    elif(len(issues) == 0):
        issue_id = await Issue.findNumber('count(id)') + 1
        issue = Issue(id = issue_id, title = title, content = content, content_md5 = content_md5, version = version,user_id=None, status = 0)
        await issue.save()
    else:
        raise APIValueError('upload', '数据库存储错误%s'%name)
   
    crash = Crash(id = name, issue_id = issue_id, crash_doc = crashDoc, app_detail = appDetail)
    await crash.save()
    
    return "success"
    