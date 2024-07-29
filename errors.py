# define Python user-defined exceptions
class UnknownContactException(Exception):
    def __init__(self, id: str):
        self.id = id

class InvalidDataTypeException(Exception):
    pass