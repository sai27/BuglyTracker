# --*-- encoding:utf-8 --*--
import logging; logging.basicConfig(level=logging.INFO)
import asyncio, os, json, time
from datetime import datetime
from aiohttp import web
import orm
from models import User

async def index(request):
    await asyncio.sleep(0.5)
    return web.Response(body=b'<h1>Awesome</h1>', content_type='text/html')

async def init(loop):
    app = web.Application(loop = loop)
    app.router.add_route('GET', '/', index)
    srv = await loop.create_server(app.make_handler(), '127.0.0.1', 8000)
    
    await orm.create_pool(loop,
        host = 'localhost',
        port = 3306,
        user = 'root',
        password = '123456',
        db = 'blog'
    )
    
    #u = User(name='Test', email='test@example.com', passwd='1234567890', image='about:blank')
    #await u.save()
    
    print('server started')
    return srv

loop = asyncio.get_event_loop()
loop.run_until_complete(init(loop))
loop.run_forever()


