#==========================================================
# BASE PYX TEMPLATE
#==========================================================

from libc.stdlib cimport malloc, free

cdef extern from "lowlevel/modules_Optimizer_c.h" nogil:
    int basic_function()

def call_basic_function():
    return basic_function()
