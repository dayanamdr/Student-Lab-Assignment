from copy import deepcopy


def sort(list_to_sort, key=None, function=None, reverse=False):
    def default_key(item):
        return item

    def default_compare(item1, item2):
        return item1 < item2

    if key is None:
        key = default_key
    if function is None:
        function = default_compare
    sorted_list = deepcopy(list_to_sort)
    pointer = 0

    while pointer < len(sorted_list):
        if pointer == 0 or not function(key(sorted_list[pointer]), key(sorted_list[pointer - 1])):
            pointer += 1
        else:
            sorted_list[pointer], sorted_list[pointer - 1] = sorted_list[pointer - 1], sorted_list[pointer]  # swap
            pointer -= 1

    if reverse is True:  # reverse the sorted_list if needed
        start_pointer = 0
        end_pointer = len(sorted_list) - 1
        while start_pointer < end_pointer:  # gnome sort - https://www.geeksforgeeks.org/gnome-sort-a-stupid-one/
            sorted_list[start_pointer], sorted_list[end_pointer] = sorted_list[end_pointer], sorted_list[start_pointer]
            start_pointer += 1
            end_pointer -= 1
    return sorted_list


def filter_list(list_to_filter, function):
    filtered_list = type(list_to_filter)()

    for item in list_to_filter:
        if function(item):
            filtered_list.append(item)

    return filtered_list


class Container:
    def __init__(self, new_list=None):
        self.key = -1 # -> do I need this?
        if new_list is None:
            new_list = list()
        self._list = new_list

    def __len__(self):
        return len(self._list)

    def __setitem__(self, key, value):
        self._list[key] = value

    def __getitem__(self, index):
        return self._list[index]

    def __delitem__(self, key):
        del self._list[key]

    def __iter__(self):
        yield from self._list
        # return from self._list

    def __next__(self):
        self.key += 1
        if self.key >= len(self._list):
            raise StopIteration
        return self._list[self.key]

    def append(self, item):
        self._list.append(item)

    def remove(self, item):
        self._list.remove(item)

    def values(self):  # should I add it to the a10 also???? + tests
        return list(self._list.values())

