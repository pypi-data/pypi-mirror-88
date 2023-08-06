from . import type
from . import _pyctyerror

class array(type.CType):
    def __init__(self,value : int):
        self.value = value
    def __str__(self):
        return f"{self.value}"