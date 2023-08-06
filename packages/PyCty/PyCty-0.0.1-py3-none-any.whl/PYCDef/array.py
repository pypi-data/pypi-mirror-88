from . import type
class array(type.CType):
    def __init__(self,value : list):
        self.value = value
    def __str__(self):
        return f"array({self.value})"