
#==========================================================
# BASE SETUP TEMPLATE
#==========================================================

from setuptools import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

sourceFiles = ['Config/ConfigLoader/ConfigLoader.pyx', 'Config/ConfigLoader/lowlevel/Config_ConfigLoader_c.c']

ext_modules = [
    Extension("ConfigLoader", 
            sources=sourceFiles),
]

for e in ext_modules:
    e.cython_directives = {"language_level": "3str"} 

setup(name = 'ConfigLoader',
    cmdclass={'build_ext': build_ext},
    ext_modules=ext_modules
    )
