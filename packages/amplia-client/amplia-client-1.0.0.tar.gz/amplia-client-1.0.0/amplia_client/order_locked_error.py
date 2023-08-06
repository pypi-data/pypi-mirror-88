from .rest_base_error import RestBaseError


class OrderLockedError(RestBaseError):

    def __init__(self, message, verb, url):
        RestBaseError.__init__(self, __name__, message, verb, url)


__all__ = ['OrderLockedError']
