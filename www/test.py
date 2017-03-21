import inspect, asyncio
from aiohttp import web


def test( *args, d, a = 5,  b, **kw ):
    print('test')
    print('a=', a)
    print('args')
    for k in args:
        print(k)
    print('b=', b)
    print('kw')
    for k, v in kw.items():
        print(k, v)
    
    
def wrapper(*args, **kw):
    print('wrapper')
    print('args')
    for k in args:
        print(k)
    print('kw')
    for k, v in kw.items():
        print(k, v)
    test(*args, **kw)
    
params = inspect.signature(test).parameters

for name, param in params.items():
    print(param.name,param.kind, param.annotation, param.default)
    
    
#test( 'aaa', 3, 4, b= 't', **{'c':{'c':5 }})

#a = not True and False
#print(a)


