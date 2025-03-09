from ..build.Grad import (call_basic_function as raw_call_basic_function)
#==========================================================
# BASE MODULE TEMPLATE
#==========================================================

from ..build.Grad import (
    call_basic_function as raw_basic_function
)

class GradModule:
    def __init__(self):
        pass

    def call_basic_function(self):
        return raw_basic_function()

def sample_function():
    instance = GradModule()
    instance.call_basic_function()
    return "basic_function worked."
