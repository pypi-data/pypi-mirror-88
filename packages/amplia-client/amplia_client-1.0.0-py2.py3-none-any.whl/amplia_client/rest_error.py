from .rest_base_error import RestBaseError


class RestError(RestBaseError):

    def __init__(self, verb, url, status_code, error_message=None):
        message = "REST action {0} {1} returned HTTP error {2}".format(verb, url, status_code)
        if error_message is not None and len(error_message) > 0:
            message += ": {0}".format(error_message)
        RestBaseError.__init__(self, __name__, message, verb, url)

        self.__status_code = status_code
        self.__error_message = error_message

    @property
    def status_code(self):
        return self.__status_code

    @status_code.setter
    def status_code(self, value):
        self.__status_code = value

    @property
    def error_message(self):
        return self.__error_message

    @error_message.setter
    def error_message(self, value):
        self.__error_message = value


__all__ = ['RestError']
