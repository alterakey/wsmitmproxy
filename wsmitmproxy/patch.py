import os

class Patch:
    def __init__(self, path):
        self.path = os.path.abspath(path)
        self.ns = {'__file__':self.path}
        with open(self.path, 'rb') as f:
            self.code = compile(f.read(), self.path, 'exec')
            exec(self.code, self.ns, self.ns)

    def call(self, funcname, *args, **kwargs):
        return self.ns[funcname](*args, **kwargs)
