#==========================================================
# BASE MODULE TEMPLATE
#==========================================================

from ..build.Field import (
    call_basic_function
)

class FieldModule:
    def __init__(self):
        pass

    def basic_function(self):
        return call_basic_function()

def sample_function():
    instance = FieldModule()
    instance.basic()
    return "basic_function worked."
