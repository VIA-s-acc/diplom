
#==========================================================
# BASE SETUP TEMPLATE
#==========================================================

from setuptools import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

sourceFiles = ['Optimization/Grad/Grad.pyx', 'Optimization/Grad/lowlevel/Optimization_Grad_c.c']

ext_modules = [
    Extension("Grad", 
            sources=sourceFiles),
]

for e in ext_modules:
    e.cython_directives = {"language_level": "3str"} 

setup(name = 'Grad',
    cmdclass={'build_ext': build_ext},
    ext_modules=ext_modules
    )
