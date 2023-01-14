import unittest
from utils_functions import sort, filter_list, Container


class SortFunctionTest(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    def test_sort__list_in_ascending_order__sorted_as_expected(self):
        list_to_sort = [3, 4, 1, 6]
        sorted_list = sort(list_to_sort)
        self.assertEqual(sorted_list, [1, 3, 4, 6])

    def test_sort__list_in_descending_order__sorted_as_expected(self):
        list_to_sort = [3, 4, 1, 6]
        sorted_list = sort(list_to_sort, reverse=True)
        self.assertEqual([6, 4, 3, 1], sorted_list)

    def test_sort__list_by_key__sorted_as_expected(self):
        list_to_sort = [[2, 3], [3, 4], [1, 4]]
        sorted_list = sort(list_to_sort, key=lambda item: item[0])
        self.assertEqual([[1, 4], [2, 3], [3, 4]], sorted_list)

    def test_sort__list_by_given_criteria__sorted_as_expected(self):
        list_to_sort = [[2, 3], [3, 4], [1, 4], [2, 1]]

        def sorting_criteria(item1, item2):
            if item1[0] < item2[0]:
                return True
            elif item1[0] == item2[0] and item1[1] < item2[1]:
                return True
            return False
        sorted_list = sort(list_to_sort, function=sorting_criteria)
        self.assertEqual([[1, 4], [2, 1], [2, 3], [3, 4]], sorted_list)


class FilterFunctionTest(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    def test_filter_list__list_with_positive_numbers__filtered_as_expected(self):
        list_to_filter = [0, -1, 3, 2, 5, -4, -1]
        filtered_list = filter_list(list_to_filter, function=lambda item: item > 0)
        self.assertEqual([3, 2, 5], filtered_list)


class ContainerClassTest(unittest.TestCase):
    def setUp(self) -> None:
        self._list_container = Container()
        for index in range(10):
            self._list_container.append(index + 1)
        self._dict_container = Container({'first': 1, 'second': 2})

    def tearDown(self) -> None:
        pass

    def test_len__list_length__as_expected(self):
        self.assertEqual(10, len(self._list_container))

    def test_getitem__get_item_from_a_given_index__with_success(self):
        item = self._list_container.__getitem__(3)  # get element from index 3
        self.assertEqual(4, item)

    def test_setitem__set_item_value_for_a_given_index__with_success(self):
        self.assertEqual(8, self._list_container.__getitem__(7))
        self._list_container.__setitem__(7, 11)
        self.assertEqual(11, self._list_container.__getitem__(7))

    def test_remove__remove_item_from_a_given_index__with_success(self):
        self.assertEqual(1, self._list_container.__getitem__(0))
        self._list_container.remove(1)
        self.assertTrue(1 != self._list_container.__getitem__(0))

    def test_delitem__delete_item_from_dict_with_a_given_key__with_success(self):
        self.assertEqual(1, self._dict_container.__getitem__('first'))
        self._dict_container.__delitem__('first')
        with self.assertRaises(KeyError):
            self._dict_container.__getitem__('first')

    def test_next__get_next_element_from_list__with_success(self):
        self._list_container.__iter__()  # set iterator
        item = next(self._list_container)
        self.assertEqual(1, item)
        item = next(self._list_container)
        self.assertEqual(2, item)

    def test_next__get_next_element_outside_the_list__throws_exception(self):
        self._list_container.__iter__()
        for index in range(10):
            next(self._list_container)
        with self.assertRaises(StopIteration):
            next(self._list_container)
