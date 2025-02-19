
#==========================================================
# BASE SETUP TEMPLATE
#==========================================================

from setuptools import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

sourceFiles = ['modules/Funcs/Funcs.pyx', 'modules/Funcs/lowlevel/modules_Funcs_c.c']

ext_modules = [
    Extension("Funcs", 
            sources=sourceFiles),
]

for e in ext_modules:
    e.cython_directives = {"language_level": "3str"} 

setup(name = 'Funcs',
    cmdclass={'build_ext': build_ext},
    ext_modules=ext_modules
    )
