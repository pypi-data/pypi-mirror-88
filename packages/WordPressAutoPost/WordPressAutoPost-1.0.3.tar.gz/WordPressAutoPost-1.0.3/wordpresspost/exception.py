# define Python user-defined exceptions
class Error(Exception):
    """Base class for other exceptions"""
    pass


class UnableToPostDealOnWordPress(Exception):
    def __init__(self, message):
        self.message = message



