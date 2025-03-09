from ..build.SGrad import (call_basic_function as raw_call_basic_function)
#==========================================================
# BASE MODULE TEMPLATE
#==========================================================

from ..build.SGrad import (
    call_basic_function as raw_basic_function
)

class SgradModule:
    def __init__(self):
        pass

    def call_basic_function(self):
        return raw_basic_function()

def sample_function():
    instance = SgradModule()
    instance.call_basic_function()
    return "basic_function worked."
