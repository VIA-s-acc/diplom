
#==========================================================
# BASE SETUP TEMPLATE
#==========================================================

from setuptools import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

sourceFiles = ['model/Optimizer/Optimizer.pyx', 'model/Optimizer/lowlevel/model_Optimizer_c.c']

ext_modules = [
    Extension("Optimizer", 
            sources=sourceFiles),
]

for e in ext_modules:
    e.cython_directives = {"language_level": "3str"} 

setup(name = 'Optimizer',
    cmdclass={'build_ext': build_ext},
    ext_modules=ext_modules
    )
