"""
Custom Exception classes for pygiftbit.
"""


class AuthError(Exception):
    """
    Error indicating an authorization
    failure.
    """
    def __init__(self, code):
        self.code = code

    def __str__(self):
        return f'AuthError: {self.code} - Authorization failed, check your API key.'

    def __repr__(self):
        return self.__str__()


class APIError(Exception):
    """
    Generic API Exception class,
    catches otherwise unhandled
    errors with the Giftbit API
    """
    def __init__(self, message, status_code):
        self.message = message
        self.status_code = status_code

    def __str__(self):
        return f'APIError: {self.status_code} - {self.message}'

    def __repr__(self):
        return self.__str__


class RegionError(Exception):
    """
    Error code for unsupported
    region.
    """
    def __init__(self, region):
        self.region = region

    def __str__(self):
        return f'Invalid region: {self.region}'

    def __repr__(self):
        return self.__str__
