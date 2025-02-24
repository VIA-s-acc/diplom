
#==========================================================
# BASE SETUP TEMPLATE
#==========================================================

from setuptools import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

sourceFiles = ['model/Field/Field.pyx', 'model/Field/lowlevel/model_Field_c.c']

ext_modules = [
    Extension("Field", 
            sources=sourceFiles),
]

for e in ext_modules:
    e.cython_directives = {"language_level": "3str"} 

setup(name = 'Field',
    cmdclass={'build_ext': build_ext},
    ext_modules=ext_modules
    )
