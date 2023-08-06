import unittest
from functional_list.list_functional_mapper import ListMapper


class TestListFunctionMapper(unittest.TestCase):

    def setUp(self):
        self.example_list = [2, 3, 4, 2]
        self.example_mapper = ListMapper(*self.example_list)

    def test_representation(self):
        self.assertEqual("List" + str(self.example_list), self.example_mapper.__repr__())

    def test_iteration(self):
        self.assertEqual(sum(self.example_list), sum(self.example_mapper))

    def test_copy(self):
        mapper_copy = self.example_mapper.copy()
        self.assertNotEqual(id(mapper_copy), id(self.example_mapper))
        self.assertEqual(mapper_copy.__repr__(), self.example_mapper.__repr__())

    def test_to_list(self):
        self.assertEqual(self.example_list, self.example_mapper.to_list())

    def test_map(self):
        expected_result_1 = [x * x for x in self.example_list]
        expected_result_2 = [str(x) + 'd' for x in self.example_list]
        result_1 = self.example_mapper.map(lambda x: x * x)
        result_2 = self.example_mapper.map(lambda x: str(x) + 'd')
        self.assertEqual("List" + str(expected_result_1), result_1.__repr__())
        self.assertEqual("List" + str(expected_result_2), result_2.__repr__())

    def test_flatten(self):
        expected_result = ListMapper(2, 3, 4, 2, 1, 5)
        element_to_flatten_1 = ListMapper(self.example_list, ListMapper(1, 5))
        element_to_flatten_2 = ListMapper(self.example_mapper, ListMapper(1, 5))
        result_1 = element_to_flatten_1.flatten
        result_2 = element_to_flatten_2.flatten
        self.assertEqual(expected_result.__repr__(), result_1.__repr__())
        self.assertEqual(expected_result.__repr__(), result_2.__repr__())

    def test_flat_map(self):
        expected_result = ListMapper('je', 'suis', 'bon', 'en', 'math', "j'aime", "l'informatique")
        result = ListMapper('je suis bon en math', 'j\'aime l\'informatique').flat_map(lambda x: x.split(' '))
        self.assertEqual(expected_result.__repr__(), result.__repr__())

    def test_reduce(self):
        expected_result = sum(self.example_list)
        result = self.example_mapper.reduce(lambda x, y: x + y)

        self.assertEqual(expected_result, result)

    def test_order_by_key(self):
        expected_result = ListMapper(("I", 1), ("a", 6), ("am", 5), ("here", 4))
        result = ListMapper(("I", 1), ("am", 5), ("here", 4), ("a", 6)).order_by_key()
        self.assertEqual(expected_result.__repr__(), result.__repr__())

    def test_group_by_key(self):
        expected_result = ListMapper(("je", ListMapper(2, 4)), ("sport", ListMapper(4)), ("aime", ListMapper(1, 2)))
        result = ListMapper(("je", 2), ("aime", 1), ("je", 4), ("aime", 2), ("sport", 4)).group_by_key()
        self.assertEqual(expected_result.order_by_key().__repr__(), result.order_by_key().__repr__())

    def test_remove(self):
        expected_result = ListMapper(2, 4, 2, 3)
        list_to_test = ListMapper(2, 3, 4, 2, 3)
        list_to_test.remove(3)
        self.assertEqual(expected_result.__repr__(), list_to_test.__repr__())

    def test_remove_all(self):
        expected_result: ListMapper = ListMapper(8, 1)
        test1 = ListMapper(2, 8, 1, 2)
        test1.remove_all(2)
        self.assertEqual(expected_result.__repr__(), test1.__repr__())

    def test_remove_index(self):
        expected_result = ListMapper(2, 3, 2, 3)
        list_to_test_1 = ListMapper(2, 3, 4, 2, 3)
        list_to_test_1.remove_index(2)
        try:
            list_to_test_1.remove_index(6)
        except IndexError:
            self.assertTrue(True)
        self.assertEqual(expected_result.__repr__(), list_to_test_1.__repr__())

    def test_remove_list_index(self):
        expected_result = ListMapper(3, 3, 7, 10)
        list_to_test_1 = ListMapper(2, 3, 2, 3, 7, 9, 10)
        list_to_test_1.remove_list_index([0, 2, 5])
        try:
            list_to_test_1.remove_list_index([0, 7, 10])
        except IndexError:
            self.assertTrue(True)
        self.assertEqual(expected_result.__repr__(), list_to_test_1.__repr__())

    def test_remove_list_value(self):
        expected_result: ListMapper = ListMapper(9, 10)
        list_to_test_1 = ListMapper(2, 3, 2, 3, 7, 9, 10)
        list_to_test_1.remove_list_value([2, 3, 7, 11])
        self.assertEqual(expected_result.__repr__(),list_to_test_1.__repr__())