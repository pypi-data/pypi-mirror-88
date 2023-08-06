"""
We will put all utils tools for the main class
into this module.
"""


class ListMapperIterator:
    """
    This class is use to able the ListMapper class to be iterable.
    """

    def __init__(self, list_mapper):
        self.current = 0
        self.max = len(list_mapper.ma_list)
        self.list = list_mapper.ma_list

    def __iter__(self):
        return self

    def __next__(self):
        if self.current >= self.max:
            raise StopIteration
        ret = self.list[self.current]
        self.current += 1
        return ret
