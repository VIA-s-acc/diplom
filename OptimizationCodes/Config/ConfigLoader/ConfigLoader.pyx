#==========================================================
# BASE PYX TEMPLATE
#==========================================================

from libc.stdlib cimport malloc, free
from libc.string cimport memcpy

cdef extern from "lowlevel/Config_ConfigLoader_c.h" nogil:
    int basic_function()

def call_basic_function():
    return basic_function()
