from . import type
from . import _pyctyerror

class array(type.CType):
    def __init__(self,value : str):
        if len(value) != 1:
            raise _pyctyerror.PyCTYError("char must be one letter")
        self.value = value
    def __str__(self):
        return f"'{self.value}'"