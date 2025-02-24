from ..build.Funcs import (call_basic_function as raw_call_basic_function)
#==========================================================
# BASE MODULE TEMPLATE
#==========================================================

from ..build.Funcs import (
    call_basic_function as raw_basic_function
)

class FuncsModule:
    def __init__(self):
        pass

    def call_basic_function(self):
        return raw_basic_function()

def sample_function():
    instance = FuncsModule()
    instance.call_basic_function()
    return "basic_function worked."
