def get_first_three_elements(lst: list) -> list:
    """
    Function to return the first three elements of a list.
    :param lst: The input list.
    :return: A list containing the first three elements.
    """
    return lst[:3]


def get_last_two_elements(lst: list) -> list:
    """
    Function to return the last two elements of a list.
    :param lst: The input list.
    :return: A list containing the last two elements.
    """
    return lst[-2:]


def reverse_list(lst: list) -> list:
    """
    Function to return the reversed version of a list.
    :param lst: The input list.
    :return: The reversed list.
    """
    return lst[::-1]


def get_even_index_elements(lst: list) -> list:
    """
    Function to return the elements of a list at even indices.
    :param lst: The input list.
    :return: A list of elements at even indices.
    """
    return lst[::2]


def get_odd_index_elements(lst: list) -> list:
    """
    Function to return the elements of a list at odd indices.
    :param lst: The input list.
    :return: A list of elements at odd indices.
    """
    return lst[1::2]


def remove_duplicates(lst: list) -> list:
    """
    Function to remove duplicates from a list.
    :param lst: The input list.
    :return: A list with duplicates removed.
    """
    return list(set(lst))


def square_elements(lst: list) -> list:
    """
    Function to return a list with each element squared.
    :param lst: The input list.
    :return: A list with squared elements.
    """
    return list(map(lambda x: x**2, lst))


def double_elements(lst: list) -> list:
    """
    Function to return a list with each element doubled.
    :param lst: The input list.
    :return: A list with doubled elements.
    """
    return list(map(lambda x: x*2, lst))


def sum_of_elements(lst: list) -> int:
    """
    Function to return the sum of all elements in a list.
    :param lst: The input list.
    :return: The sum of the elements.
    """
    return sum(lst)


def is_sorted(lst: list) -> bool:
    """
    Function to check if a list is sorted in ascending order.
    :param lst: The input list.
    :return: True if the list is sorted, False otherwise.
    """
    return lst == sorted(lst)


def count_occurrences(lst: list, element) -> int:
    """
    Function to count the occurrences of an element in a list.
    :param lst: The input list.
    :param element: The element to count.
    :return: The number of occurrences of the element.
    """
    return lst.count(element)


def find_maximum(lst: list) -> int:
    """
    Function to find the maximum element in a list.
    :param lst: The input list.
    :return: The maximum element in the list.
    """
    if not lst:
        return None
    return max(lst)


def find_minimum(lst: list) -> int:
    """
    Function to find the minimum element in a list.
    :param lst: The input list.
    :return: The minimum element in the list.
    """
    if not lst:
        return None
    return min(lst)


def combine_lists(lst1: list, lst2: list) -> list:
    """
    Function to combine two lists into one.
    :param lst1: The first list.
    :param lst2: The second list.
    :return: A list containing elements from both lists.
    """
    lst1.extend(lst2)
    return lst1


def is_palindrome(lst: list) -> bool:
    """
    Function to check if a list is a palindrome.
    A list is a palindrome if it reads the same backward as forward.
    :param lst: The input list.
    :return: True if the list is a palindrome, False otherwise.
    """
    return lst == reverse_list(lst)
    # return lst == lst[::-1]

# def combine_lists(lst1, lst2):
#     return lst1 + lst2

# def is_palindrome(lst):
#     return lst == lst[::-1]
