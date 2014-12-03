from distutils.core import setup, Extension

module1 = Extension('stack', sources = ['stack.c'])

setup (name = 'stack', 
       version = '1.0',
       description = 'Linked list based stack implementation',
       ext_modules = [module1])
