class PaginatedSearchResponse(object):

    def __init__(self, model, item_constructor):
        self.__items = []
        self.__total_count = model.get('totalCount', None)

        if item_constructor is None:
            raise Exception('No constructor was provider')

        if model.get('items', None) is None:
            for item in model.get('items'):
                self.__items += item_constructor(item)
                
    @property
    def items(self):
        return self.__items
    
    @items.setter
    def items(self, value):
        self.__items = value
        
    @property
    def total_count(self):
        return self.__total_count
    
    @total_count.setter
    def total_count(self, value):
        self.__total_count = value


__all__ = ['PaginatedSearchResponse']
