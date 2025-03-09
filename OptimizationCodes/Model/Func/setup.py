
#==========================================================
# BASE SETUP TEMPLATE
#==========================================================

from setuptools import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

sourceFiles = ['Model/Func/Func.pyx', 'Model/Func/lowlevel/Model_Func_c.c']

ext_modules = [
    Extension("Func", 
            sources=sourceFiles),
]

for e in ext_modules:
    e.cython_directives = {"language_level": "3str"} 

setup(name = 'Func',
    cmdclass={'build_ext': build_ext},
    ext_modules=ext_modules
    )
