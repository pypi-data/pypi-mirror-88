from .pagination_orders import PaginationOrders


class PaginatedSearchParams(object):
    DEFAULT_LIMIT = 10

    def __init__(self):
        self.__q = ''
        self.__limit = PaginatedSearchParams.DEFAULT_LIMIT
        self.__offset = 0
        self.__order = PaginationOrders.ASC

    @property
    def q(self):
        return self.__q

    @q.setter
    def q(self, value):
        self.__q = value

    @property
    def limit(self):
        return self.__limit

    @limit.setter
    def limit(self, value):
        self.__limit = value

    @property
    def offset(self):
        return self.__offset

    @offset.setter
    def offset(self, value):
        self.__offset = value

    @property
    def order(self):
        return self.__order

    @order.setter
    def order(self, value):
        self.__order = value


__all__ = ['PaginatedSearchParams']
