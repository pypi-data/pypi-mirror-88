from .rest_base_error import RestBaseError


class RestUnreachableError(RestBaseError):

    def __init__(self, verb, url):
        RestBaseError.__init__(self, __name__, "REST action {0} {1} unreachable".format(verb, url), verb, url)


__all__ = ['RestUnreachableError']
