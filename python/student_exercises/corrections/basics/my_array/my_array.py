# from functools import reduce


def sum(tableau: list[int]) -> int:  # O(n)
    """
    Function that returns the sum of the elements of the array
    :param tableau: the array to sum
    :return: the sum of the elements of the array
    """
    # total: int = 0
    # for elem in tableau:
    #     total += elem
    # return total

    total: int = 0
    for i in range(len(tableau)):
        total += tableau[i]
    return total


def average(tableau: list[int]) -> float:  # O(n)
    """
    Function that returns the average of the elements of the array
    :param tableau: the array to average
    :return: the average of the elements of the array
    """
    # return sum(tableau) / len(tableau)
    total: int = 0
    count: int = 0
    for elem in tableau:
        total += elem
        count += 1

    if count != 0:
        return total / count


def min(tableau: list[int]) -> int:  # O(n)
    """
    Function that returns the minimum of the elements of the array
    :param tableau: the array to find the minimum of
    :return: the minimum of the elements of the array
    """
    min_: int = tableau[0]
    for i in tableau[1:]:
        if i < min_:
            min_ = i
    return min_


def max(tableau: list[int]) -> int:  # O(n)
    """
    Function that returns the maximum of the elements of the array
    :param tableau: the array to find the maximum of
    :return: the maximum of the elements of the array
    """
    max_: int = tableau[0]
    for i in tableau[1:]:
        if i > max_:
            max_ = i
    return max_


def min_max(tableau: list[int]) -> tuple[int, int]:  # O(2n)
    """
    Function that returns the minimum and maximum of the elements of the array
    :param tableau: the array to find the minimum and maximum of
    :return: the minimum and maximum of the elements of the array
    """
    # return (min(tableau), max(tableau))
    max_ = min_ = tableau[0]
    for i in tableau[1:]:
        if i > max_:
            max_ = i
        elif i < min_:
            min_ = i
    return min_, max_


def mode(tableau: list[int]) -> int:  # O(n^2)
    """
    Function that returns the mode of the elements of the array
    The mode is the value that appears most often in a set of data values.
    If there is a tie, the mode is the smallest value.
    :param tableau: the array to find the mode of
    :return: the mode of the elements of the array
    """
    # if tableau == []:
    #     return None

    # mode_value: int = tableau[0]
    # mode_count: int = 0

    # for value in tableau:
    #     count = 0
    #     for i in tableau:
    #         if i == value:
    #             count += 1
    #     if count > mode_count:
    #         mode_count = count
    #         mode_value = value
    #     elif count == mode_count and value < mode_value:
    #         mode_value = value
    # return mode_value

    occurences: dict[int, int] = {}
    for value in tableau:
        # if value in occurences:
        #     occurences[value] = occurences[value] + 1
        # else:
        #     occurences[value] = 0 + 1
        occurences[value] = occurences.get(value, 0) + 1

    max_occur: int = max(list(occurences.values()))
    maximus: list[int] = []
    for k, v in occurences.items():
        if v == max_occur:
            maximus.append(k)

    return min(maximus)


def variance(tableau: list[int]) -> float:  # O(n) -> O(n^2)
    """
    Function that returns the variance of the elements of the array
    :param tableau: the array to find the variance of
    :return: the variance of the elements of the array
    """
    # variance = 1/n * sum((Xi-X_bar)**2)
    # n = len(tableau)
    # x_bar = mean(tableau)
    # xi = each values

    n: float = len(tableau)
    x_bar: float = average(tableau)
    sum_: int = 0

    for xi in tableau:
        sum_ += (xi - x_bar) ** 2
    return sum_ / n


def standard_deviation(tableau: list[int]) -> float:
    """
    Function that returns the standard deviation of the elements of the array
    The standard deviation is the square root of the variance.
    :param tableau: the array to find the standard deviation of
    :return: the standard deviation of the elements of the array
    """
    return variance(tableau) ** (1 / 2)


def exist(tableau: list[int], valeur: int) -> bool:
    """
    Function that returns True if the value exists in the array
    :param tableau: the array to check if the value exists in
    :param valeur: the value to check if it exists in the array
    :return: True if the value exists in the array, False otherwise
    """
    # for value in tableau:
    #     if value == valeur:
    #         return True
    # return False
    return valeur in tableau


def position(tableau: list[int], valeur: int) -> int:
    """
    Function that returns the position of the first value in the array
    If the value does not exist in the array, it returns -1
    :param tableau: the array to find the position of
    :param valeur: the value to find the position of
    :return: the position of the value in the array
    """
    for idx, val in enumerate(tableau):
        if val == valeur:
            return idx
    return -1


def similars(arr1: list[int], arr2: list[int]) -> bool:  # O(n)
    """
    Function that returns True if the two arrays are similar
    :param arr1: the first array
    :param arr2: the second array
    :return: True if the two arrays are similar, False otherwise
    """
    if len(arr1) != len(arr2):
        return False

    for i in range(len(arr1)):
        if arr1[i] != arr2[i]:
            return False
    return True
    return arr1 == arr2


def is_list(tableau) -> bool:  # O(1)
    """
    Function that returns True if the array is a table
    :param tableau: the array to check if it is a table
    :return: True if the array is a table, False otherwise
    """
    return type(tableau) == list


def is_list_of_numbers(tableau) -> bool:  # O(n)
    """
    Function that returns True if the array is a table of numbers
    :param tableau: the array to check if it is a table of numbers
    :return: True if the array is a table of numbers, False otherwise
    """
    if not is_list(tableau):
        return False

    if len(tableau) == 0:
        return False

    for elem in tableau:
        if type(elem) not in (int, float):
            return False
    return True


def sort_ascending(arr: list[int]) -> list[int]:  # O(n^2); O(n*log(n))
    """
    Function that returns the sorted array in ascending order
    :param arr: the array to sort
    :return: the sorted array in ascending order
    """
    sorted_array: list[int] = arr[:]
    for i in range(len(sorted_array) - 1):
        for j in range(i + 1, len(sorted_array)):
            if sorted_array[j] < sorted_array[i]:
                sorted_array[i], sorted_array[j] = (sorted_array[j], sorted_array[i])
    return sorted_array


def sort_descending(arr: list[int]) -> list[int]:  # O(n^2)
    """
    Function that returns the sorted array in descending order
    :param arr: the array to sort
    :return: the sorted array in descending order
    """
    sorted_array: list[int] = arr[:]
    for i in range(len(sorted_array) - 1):
        for j in range(i + 1, len(sorted_array)):
            if sorted_array[j] > sorted_array[i]:
                sorted_array[i], sorted_array[j] = (sorted_array[j], sorted_array[i])
    return sorted_array


def median(tableau: list[int]) -> float:  # O(n^2)
    """
    Function that returns the median of the elements of the array
    :param tableau: the array to find the median of
    :return: the median of the elements of the array
    """
    sorted_array: list[int] = sort_ascending(tableau)
    mid: int = len(sorted_array) // 2

    if len(sorted_array) % 2 == 0:
        return (sorted_array[mid - 1] + sorted_array[mid]) / 2
    return float(sorted_array[mid])
