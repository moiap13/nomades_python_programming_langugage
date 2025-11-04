def sum(tableau: list[int]) -> int:  # O(n)
    """
    Function that returns the sum of the elements of the array

    :param tableau: the array to sum

    :return: the sum of the elements of the array
    """
    sum_: int = 0
    for number in tableau:
        sum_ += number
    return sum_


def average(tableau: list[int]) -> float:  # O(n)
    """
    Function that returns the average of the elements of the array
    :param tableau: the array to average
    :return: the average of the elements of the array
    """
    return sum(tableau) / len(tableau)


def min(tableau: list[int]) -> int:
    """
    Function that returns the minimum of the elements of the array
    :param tableau: the array to find the minimum of
    :return: the minimum of the elements of the array
    """
    # O(n^3)
    # while len(tableau) > 1:  # O(n)
    #     for i in tableau:  # O(n)
    #         for y in range(0, len(tableau)):  # O(n)
    #             if i > tableau[y]:  # O(1)
    #                 try:  # O(1)
    #                     tableau.remove(i)  # O(1)
    #                     break
    #                 except:
    #                     pass
    #             # else:
    #             #     pass
    # return tableau[0]

    # tab = sort_ascending(tableau)  # O(n^2)
    # return tab[0]

    # min_: int = tableau[0]
    # for i in tableau[1:]:
    #     if i < min_:
    #         min_ = i
    # return min_

    min_: int = tableau[0]  # O(n)
    for i in range(1, len(tableau)):
        if tableau[i] < min_:
            min_ = tableau[i]
    return min_


def max(tableau: list[int]) -> int:
    """
    Function that returns the maximum of the elements of the array
    :param tableau: the array to find the maximum of
    :return: the maximum of the elements of the array
    """
    max_: int = tableau[0]  # O(n)
    for i in range(1, len(tableau)):
        if tableau[i] > max_:
            max_ = tableau[i]
    return max_


def min_max(tableau: list[int]) -> tuple[int, int]:
    """
    Function that returns the minimum and maximum of the elements of the array
    :param tableau: the array to find the minimum and maximum of
    :return: the minimum and maximum of the elements of the array
    """
    return min(tableau), max(tableau)


def mode(tableau: list[int]) -> int:  # O(n)
    """
    Function that returns the mode of the elements of the array
    The mode is the value that appears most often in a set of data values.
    If there is a tie, the mode is the smallest value.
    :param tableau: the array to find the mode of
    :return: the mode of the elements of the array
    """
    # 1: count the number occurence in list
    freqs: dict[int, int] = {}
    for number in tableau:
        # if number in freqs:
        #     freqs[number] += 1
        # else:
        #     freqs[number] = 1

        # if number not in freqs:
        #     freqs[number] = 0
        # freqs[number] += 1

        # if number in freqs:
        #     freqs[number] = freqs[number] + 1
        # else:
        #     freqs[number] = 0 + 1

        freqs[number] = freqs.get(number, 0) + 1

    # 2. Get the maximum number of occurence
    max_occurences: int = max(list(freqs.values()))

    # 3. get the numbers that appear the max occurence number
    max_numbers: list[int] = []

    for k, v in freqs.items():
        if v == max_occurences:
            max_numbers.append(k)

    # 4. return the lowest value from the max occurence number
    return min(max_numbers)


def variance(tableau: list[int]) -> float:
    """
    Function that returns the variance of the elements of the array
    :param tableau: the array to find the variance of
    :return: the variance of the elements of the array
    """
    sum_: float = 0.0
    x_bar: float = average(tableau)
    for xi in tableau:
        sum_ += (xi - x_bar) ** 2
    return sum_ / len(tableau)


def standard_deviation(tableau: list[int]) -> float:
    """
    Function that returns the standard deviation of the elements of the array
    The standard deviation is the square root of the variance.
    :param tableau: the array to find the standard deviation of
    :return: the standard deviation of the elements of the array
    """
    import math

    return math.sqrt(variance(tableau))
    return variance(tableau) ** (1 / 2)


def exist(tableau: list[int], valeur: int) -> bool:
    """
    Function that returns True if the value exists in the array
    :param tableau: the array to check if the value exists in
    :param valeur: the value to check if it exists in the array
    :return: True if the value exists in the array, False otherwise
    """
    return valeur in tableau  # O(n)

    for number in tableau:
        if number == valeur:
            return True
    return False


def position(tableau: list[int], valeur: int) -> int:
    """
    Function that returns the position of the first value in the array
    If the value does not exist in the array, it returns -1
    :param tableau: the array to find the position of
    :param valeur: the value to find the position of
    :return: the position of the value in the array
    """
    for i in range(len(tableau)):
        if tableau[i] == valeur:
            return i
    return -1


def similars(arr1: list[int], arr2: list[int]) -> bool:
    """
    Function that returns True if the two arrays are similar
    :param arr1: the first array
    :param arr2: the second array
    :return: True if the two arrays are similar, False otherwise
    """
    # if len(arr1) != len(arr2):
    #     return False

    # for i in range(len(arr1)):
    #     if arr1[i] != arr2[i]:
    #         return False

    # return True

    return arr1 == arr2


def is_list(tableau: any) -> bool:
    """
    Function that returns True if the array is a table
    :param tableau: the array to check if it is a table
    :return: True if the array is a table, False otherwise
    """
    return type(tableau) == list


def is_list_of_numbers(tableau: any) -> bool:
    """
    Function that returns True if the array is a table of numbers
    :param tableau: the array to check if it is a table of numbers
    :return: True if the array is a table of numbers, False otherwise
    """
    if (not is_list(tableau)) or len(tableau) == 0:
        return False

    for item in tableau:
        if type(item) not in (int, float):
            return False

    return True


def sort_ascending(arr: list[int]) -> list[int]:
    """
    Function that returns the sorted array in ascending order
    :param arr: the array to sort
    :return: the sorted array in ascending order
    """
    arr_sorted: list[int] = arr.copy()

    for i in range(0, len(arr_sorted) - 1):
        for j in range(i + 1, len(arr_sorted)):
            if arr_sorted[i] > arr_sorted[j]:
                # temp: int = arr_sorted[i]
                # arr_sorted[i] = arr_sorted[j]
                # arr_sorted[j] = temp

                arr_sorted[i], arr_sorted[j] = (arr_sorted[j], arr_sorted[i])
    return arr_sorted


def sort_descending(arr: list[int]) -> list[int]:
    """
    Function that returns the sorted array in descending order
    :param arr: the array to sort
    :return: the sorted array in descending order
    """
    arr_sorted: list[int] = arr.copy()

    for i in range(0, len(arr_sorted) - 1):
        for j in range(i + 1, len(arr_sorted)):
            if arr_sorted[i] < arr_sorted[j]:
                # temp: int = arr_sorted[i]
                # arr_sorted[i] = arr_sorted[j]
                # arr_sorted[j] = temp

                arr_sorted[i], arr_sorted[j] = (arr_sorted[j], arr_sorted[i])
    return arr_sorted


def median(tableau: list[int]) -> float:
    """
    Function that returns the median of the elements of the array
    :param tableau: the array to find the median of
    :return: the median of the elements of the array
    """
    sorted_array: list[int] = sort_ascending(tableau)
    mid: int = len(sorted_array) // 2
    return (
        float(sorted_array[mid])
        if len(tableau) % 2 == 1
        else (sorted_array[mid] + sorted_array[mid - 1]) / 2
    )
