
#==========================================================
# BASE SETUP TEMPLATE
#==========================================================

from setuptools import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

sourceFiles = ['Optimization/SGrad/SGrad.pyx', 'Optimization/SGrad/lowlevel/Optimization_SGrad_c.c']

ext_modules = [
    Extension("SGrad", 
            sources=sourceFiles),
]

for e in ext_modules:
    e.cython_directives = {"language_level": "3str"} 

setup(name = 'SGrad',
    cmdclass={'build_ext': build_ext},
    ext_modules=ext_modules
    )
