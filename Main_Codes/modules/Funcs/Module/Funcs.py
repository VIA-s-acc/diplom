#==========================================================
# BASE MODULE TEMPLATE
#==========================================================

from ..build.Funcs import (
    call_basic_function
)

class FuncsModule:
    def __init__(self):
        pass

    def basic_function(self):
        return call_basic_function()

def sample_function():
    instance = FuncsModule()
    instance.basic()
    return "basic_function worked."
