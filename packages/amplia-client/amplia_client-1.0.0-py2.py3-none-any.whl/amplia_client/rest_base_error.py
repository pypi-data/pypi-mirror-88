class RestBaseError(Exception):

    def __init__(self, name, message, verb, url):
        super(RestBaseError, self).__init__(message)
        self.__name = name
        self.__verb = verb
        self.__url = url

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        self.__name = value

    @property
    def verb(self):
        return self.__verb

    @verb.setter
    def verb(self, value):
        self.__verb = value

    @property
    def url(self):
        return self.__url

    @url.setter
    def url(self, value):
        self.__url = value


__all__ = ['RestBaseError']
