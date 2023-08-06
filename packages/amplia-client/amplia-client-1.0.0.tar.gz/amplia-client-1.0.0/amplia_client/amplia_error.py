from .rest_base_error import RestBaseError


class AmpliaError(RestBaseError):

    def __init__(self, verb, url, error_code, error_message):
        message = "Amplia API error {0}".format(error_code)
        if message is not None:
            message += ": {0}".format(error_message)
        RestBaseError.__init__(self, __name__, message, verb, url)

        self.__error_code = error_code
        self.__error_message = error_message

    @property
    def error_code(self):
        return self.__error_code

    @error_code.setter
    def error_code(self, value):
        self.__error_code = value

    @property
    def error_message(self):
        return self.__error_message

    @error_message.setter
    def error_message(self, value):
        self.__error_message = value


__all__ = ['AmpliaError']
