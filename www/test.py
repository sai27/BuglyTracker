class A(dict):
    def __init__(self, **kw):
        super().__init__(**kw)
        
    def __getattr__(self, key):
        print('shit')

    def __setattr__(self, key, value):
        self[key] = value
        
    def __getitem__(self, key):
        print('shit2')
        
a = A(s = '123')
print(a.s)
a['s']
print(dir(dict))

print('.'.join(['a','b','c']))