"""
This module will allow us to build
an object list that will have
a functional programming behavior.

The main class is the ListMapper
that contains a lot of method
"""

import sys
from typing import Any, List

from functional_list.utils.tools_for_main_class import ListMapperIterator

sys.setrecursionlimit(150000)


class ListMapper:
    """
    This class object aim to emulate the same behavior of a list object
    but the difference is that we will use it to make a functionnal
    programming.
    """

    def __init__(self, *args):
        self.ma_list = list(args)

    def __str__(self):
        return 'List' + str(self.ma_list)

    def __repr__(self):
        return self.__str__()

    def __iter__(self):
        return ListMapperIterator(self)

    def __setitem__(self, idx, data):
        self.ma_list[idx] = data

    def __getitem__(self, idx):
        return self.ma_list[idx]

    def copy(self) -> "ListMapper":
        """
        Copy a ListMapper
        :return: an object of ListMapper type
        """
        temp = self.ma_list[:]
        return ListMapper(*temp)

    def to_list(self) -> List[Any]:
        """
        :return a list
        Example:
        >> ListMapper(1,2).tolist()
        >> [1,2]
        """
        return self.ma_list

    def map(self, function) -> "ListMapper":
        """
          :function a function as params
          :return ListMapper
          Example:
          >> test=ListMapper(2,3,4)
          >> test.map(lambda x:x*x)
          >> List[4, 9, 16]
        """
        res: ListMapper = self.copy()
        res.ma_list = list(map(function, self.ma_list))
        return res

    @property
    def flatten(self) -> "ListMapper":
        """
        :return ListMapper
        Example:
        >> test = ListMapper([1,2,4], ListMapper(3,5,6))
        >> test.flatten()
        >> List[1, 2, 4, 3, 5, 6]
        """
        res = self.copy()
        args = [list(val) if isinstance(val, ListMapper) else val for val in self.ma_list]
        res.ma_list = sum(args, [])
        return res

    def flat_map(self, function) -> "ListMapper":
        """
        :param function: function
        :return: ListMapper
        Example:
        >> test = ListMapper("where are you?","I am here")
        >> test.flat_map(lambda x: x.split(" ")
        >> List["where","are","you","I","am","here"]
        """
        temp = self.map(function).ma_list[:]
        res = self.copy()
        res.ma_list = temp
        return res.flatten

    def reduce(self, function) -> Any:
        """
        :param function:
        :return: Any
        Example:
        >> test=ListMapper(1,2,3,4)
        >> test.reduce(lambda x,y:x+y)
        >> 10
        """
        result = self.ma_list[0]
        for k in range(1, len(self.ma_list)):
            result = function(self.ma_list[k], result)
        return result

    def order_by_key(self):
        """
        :return: ListMapper
        Example:
        >> test = ListMapper(("I", 1), ("a", 6), ("am", 5), ("here", 4))
        >> test.reduce_by_key()
        >> List[('I', 1), ('a', 6), ('am', 5), ('here', 4)]
        """
        temp = sorted(self.ma_list)
        res = self.copy()
        res.ma_list = temp
        return res

    def group_by_key(self):
        """
        :return: ListMapper
        Example:
        >> test= ListMapper(("I",2),("am",1),("here",1),("here",4),("am",1),("I",1))
        >> test.group_by_key()
        >> List[("I",List[2,1]),("am",List[1, 1]),("here",List[4,1]))
        """
        to_map_list = self.map(lambda x: x)
        res = to_map_list.map(lambda x: x[0]).unique
        res = res.map(
            lambda x: (x, to_map_list.map(lambda y: y[1] if x == y[0] else None)
                       .filter(lambda x: x is not None))
        )

        return res

    def reduce_by_key(self, function) -> "ListMapper":
        """
        :param function:
        :return: ListMapper
        Example:
        >> test= ListMapper(("I",2),("am",1),("here",1),("here",4),("am",1),("I",1))
        >> test.reduce_by_key(lambda x,y:x+y)
        >> List[("I",3),("am",2),("here",5)]
        """
        return self.group_by_key().map(lambda x: (x[0], x[1].reduce(function)))

    def foreach(self, function):
        """
        :param function:
        :return:
        Example:
        >> test=ListMapper(1,2,3)
        >> test.foreach(lambda x: print("the value equals={}".format(x)))
        >> "the value equals=1"
        >> "the value equals=2"
        >>  "the value equals=3"
        """
        for k in self:
            function(k)

    @property
    def unique(self):
        """
        :return: ListMapper
        Example:
        >> test = ListMapper(1,2,3,3,2,1)
        >> test.unique
        >> List[1, 2, 3]
        """
        res = self.copy()
        res.ma_list = list(set(self.ma_list))
        return res

    def filter(self, function) -> "ListMapper":
        """
        :param function:
        :return: ListMapper
        Example:
        >> test=ListMapper(1,2,3,4,5,6)
        >> test.filter(lambda x: x%2==0)
        >> List[2, 4, 6]
        """
        res = self.copy()
        res.ma_list = list(filter(function, self.ma_list))
        return res

    def append(self, value):
        """
        :param value: Element to append
        :return: ListMapper
        example:
        >> test = ListMapper(1,2,3)
        >> test.append(4)
        >> List[1, 2, 3, 4]
        """
        self.ma_list.append(value)
        return self

    def extend(self, *list_value) -> "ListMapper":
        """
        :param list_value: list python of element
        :return: ListMapper
        example:
        >> test1 = ListMapper(1,2,3)
        >> test2 = [4,5,6]
        >> test1.append(*test2)
        >> List[1, 2, 3, 4, 5, 6]
        """
        self.ma_list.extend(list_value)
        return self

    def insert(self, index: int, value: Any) -> "ListMapper":
        """
        :param index: index to insert
        :param value: the new value
        :return: ListMapper
        example:
        >> test = ListMapper(1,2,3)
        >> test.insert(1,4)
        >> List[1, 4, 2, 3, 4]
        """
        self.ma_list.insert(index, value)
        return self

    @property
    def head(self) -> Any:
        """
        :return Any
        Example:
        >> test=ListMapper(10,30,42,89)
        >> test.head
        >> 10
        """
        return self.ma_list[0]

    @property
    def tail(self):
        """
        :return Any
        Example:
        >> test=ListMapper(10,30,42,89)
        >> test.head
        >> 89
        """
        return self.ma_list[-1]

    def remove(self, elem: Any) -> None:
        """

        :param elem:
        :return:
        Example:
        >> test = ListMapper(2,8,1,8)
        >> test.remove(8)
        >> print(test)
        >> List[2, 8, 1]
        """
        self.ma_list.remove(elem)

    def remove_all(self, value: Any) -> "ListMapper":
        """
        This method remove all value equals to value in
        the ListMapper
        :param value: ListMapper(Any)
        :return:
        Example:
        >> test1 = ListMapper(2, 8, 1, 2)
        >> test2 = 2
        >> test1.remove_all(test2)
        >> List[8, 1]
        """
        self.ma_list = [val for val in self.ma_list if val != value]
        return self

    def remove_index(self, index: int) -> "ListMapper":
        """
        :param: index: index of an element
        :return: ListMapper
        Example:
        >> test = ListMapper(3,4,8,5)
        >> test.remove_index(3)
        >> List[3, 4, 5]
        """
        if len(self.ma_list) <= index:
            raise IndexError('list index out of range')
        self.ma_list = [k for i, k in enumerate(self.ma_list) if i != index]
        return self

    def remove_list_index(self, list_index: List[int]) -> "ListMapper":
        """
        :param list_index:
        :return: ListMapper
        Example:
        >> test = ListMapper(2,4,3,7,8,19,2)
        >> list_to_remove = [0, 3, 5]
        >> test.remove_list_index(list_to_remove)
        >> List[4, 3, 7, 8, 2]
        """
        nb_element = len(self.ma_list)
        sum_elem = sum(k >= nb_element for k in list_index)
        if sum_elem > 0:
            raise IndexError('list index out of range')
        self.ma_list = [k for i, k in enumerate(self.ma_list) if i not in list_index]
        return self

    def remove_list_value(self, list_value: List[Any]) -> "ListMapper":
        """
        :param list_value:
        :return: ListMapper
        Example:
        >> test = ListMapper(1,2,3,4,5)
        >> list_element_to_remove=[1, 3, 5]
        >> test.remove_list_value(list_element_to_remove)
        >> List[2, 4]
        """
        self.ma_list = [val for val in self.ma_list if val not in list_value]
        return self
