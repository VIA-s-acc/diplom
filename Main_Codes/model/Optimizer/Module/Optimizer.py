from ..build.Optimizer import (call_basic_function as raw_call_basic_function)
#==========================================================
# BASE MODULE TEMPLATE
#==========================================================

from ..build.Optimizer import (
    call_basic_function as raw_basic_function
)

class OptimizerModule:
    def __init__(self):
        pass

    def call_basic_function(self):
        return raw_basic_function()

def sample_function():
    instance = OptimizerModule()
    instance.call_basic_function()
    return "basic_function worked."
