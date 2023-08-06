# define Python user-defined exceptions
class Error(Exception):
    """Base class for other exceptions"""
    pass


class ProductIsOutOfStock(Exception):
    def __init__(self, message):
        self.message = message


class UnableToGetProductInformation(Exception):
    def __init__(self, message):
        self.message = message


class UnableToSupportDomain(Exception):
    def __init__(self, message):
        self.message = message


class UnableToGetProductId(Exception):
    def __init__(self, message):
        self.message = message
