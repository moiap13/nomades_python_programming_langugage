def sum(tableau: list[int]) -> int: # O(n)
    """
    Function that returns the sum of the elements of the array
    :param tableau: the array to sum
    :return: the sum of the elements of the array
    """
    total: int = 0

    for elem in tableau:
        total += elem # total = total + elem
    
    return total


def average(tableau: list[int]) -> float: # O(n)
    """
    Function that returns the average of the elements of the array
    :param tableau: the array to average
    :return: the average of the elements of the array
    """
    return sum(tableau) / len(tableau)


def min(tableau: list[int]) -> int: # O(n)
    """
    Function that returns the minimum of the elements of the array
    :param tableau: the array to find the minimum of
    :return: the minimum of the elements of the array
    """
    min_: int = tableau[0]

    for idx in range(1, len(tableau)):
        elem: int = tableau[idx]
        if elem < min_:
            min_ = elem

    return min_


def max(tableau: list[int]) -> int: # O(n)
    """
    Function that returns the maximum of the elements of the array
    :param tableau: the array to find the maximum of
    :return: the maximum of the elements of the array
    """
    max_: int = tableau[0]

    for idx in range(1, len(tableau)):
        elem: int = tableau[idx]
        if elem > max_:
            max_ = elem

    return max_


def min_max(tableau: list[int]) -> tuple[int, int]: # O(n)
    """
    Function that returns the minimum and maximum of the elements of the array
    :param tableau: the array to find the minimum and maximum of
    :return: the minimum and maximum of the elements of the array
    """

    min_: int = tableau[0]
    max_: int = tableau[0]

    for idx in range(1, len(tableau)):
        elem: int = tableau[idx]
        if elem < min_:
            min_ = elem
        if elem > max_:
            max_ = elem

    return min_, max_

    return min(tableau), max(tableau)

def mode(tableau: list[int]) -> int:
    """
    Function that returns the mode of the elements of the array
    The mode is the value that appears most often in a set of data values.
    If there is a tie, the mode is the smallest value.
    :param tableau: the array to find the mode of
    :return: the mode of the elements of the array
    """
    return None

def variance(tableau: list[int]) -> float: # O(n**2) -> O(n)
    """
    Function that returns the variance of the elements of the array
    :param tableau: the array to find the variance of
    :return: the variance of the elements of the array
    """
    total: int = 0                          # O(1)
    avg: float = average(tableau)           # O(n)

    for xi in tableau:                      # O(n) -> O(n)
        total += (xi-avg)**2                  # O(1)
    
    return total / len(tableau)             # O(n)


def standard_deviation(tableau: list[int]) -> float:
    """
    Function that returns the standard deviation of the elements of the array
    The standard deviation is the square root of the variance.
    :param tableau: the array to find the standard deviation of
    :return: the standard deviation of the elements of the array
    """
    import math
    return math.sqrt(variance(tableau))
    return variance(tableau)**(1/2)


def exist(tableau: list[int], valeur: int) -> bool:
    """
    Function that returns True if the value exists in the array
    :param tableau: the array to check if the value exists in
    :param valeur: the value to check if it exists in the array
    :return: True if the value exists in the array, False otherwise
    """
    return valeur in tableau

    for elem in tableau:
        if elem == valeur:
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
    for idx, elem in enumerate(tableau):
        if elem == valeur:
            return idx
    return -1
    
    for idx in range(len(tableau)):
        elem: int = tableau[idx]
        if elem == valeur:
            return idx
    return -1

def similars(arr1: list[int], arr2: list[int]) -> bool:
    """
    Function that returns True if the two arrays are similar
    :param arr1: the first array
    :param arr2: the second array
    :return: True if the two arrays are similar, False otherwise
    """
    if len(arr1) == len(arr2):
        for idx in range(len(arr1)):
          if arr1[idx] != arr2[idx]:
              return False
        return True
    return False

    if len(arr1) != len(arr2):
      return False

    assert len(arr1) == len(arr2)

    for idx in range(len(arr1)):
      if arr1[idx] != arr2[idx]:
          return False
    return True

def is_list(tableau) -> bool:
    """
    Function that returns True if the array is a table
    :param tableau: the array to check if it is a table
    :return: True if the array is a table, False otherwise
    """
    return type(tableau) == list


def is_list_of_numbers(tableau) -> bool:
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
        if type(elem) != int:
            return False
    return True


def sort_ascending(arr: list[int]) -> list[int]:
    """
    Function that returns the sorted array in ascending order 
    :param arr: the array to sort
    :return: the sorted array in ascending order
    """
    for i in range(len(arr)-1):
        for j in range(i+1, len(arr)):
            if arr[j] < arr[i]:
                arr[i], arr[j] = arr[j], arr[i]

                # tmp: int = arr[i]
                # arr[i] = arr[j]
                # arr[j] = tmp
    return arr


def sort_descending(arr: list[int]) -> list[int]:
    """
    Function that returns the sorted array in descending order 
    :param arr: the array to sort
    :return: the sorted array in descending order
    """
    for i in range(len(arr)-1):
        for j in range(i+1, len(arr)):
            if arr[j] > arr[i]:
                arr[i], arr[j] = arr[j], arr[i]
    return arr


def median(tableau: list[int]) -> int:
    """
    Function that returns the median of the elements of the array
    :param tableau: the array to find the median of
    :return: the median of the elements of the array
    """
    sorted_tableau: list[int] = sort_ascending(tableau)
    mid: int = len(sorted_tableau) // 2
    if len(sorted_tableau) % 2 == 1:
        return sorted_tableau[mid]

    return (sorted_tableau[mid-1] + sorted_tableau[mid]) / 2
        
