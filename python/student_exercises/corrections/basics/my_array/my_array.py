from functools import reduce

def sum(tableau: list[int]) -> int:
    """
    Function that returns the sum of the elements of the array
    :param tableau: the array to sum
    :return: the sum of the elements of the array
    """
    # sum_: int = 0
    # for elem in tableau:
    #     sum_ += elem
    # return sum_

    return reduce(lambda acc, value: acc + value, tableau, 0)



def average(tableau: list[int]) -> float:
    """
    Function that returns the average of the elements of the array
    :param tableau: the array to average
    :return: the average of the elements of the array
    """
    # return sum(tableau) / len(tableau)
    # return sum(map(lambda x: x/len(tableau), tableau))

    avg: float = 0.0
    for elem in tableau:
        avg += elem / len(tableau)
    return avg


def min(tableau: list[int]) -> int:
    """
    Function that returns the minimum of the elements of the array
    :param tableau: the array to find the minimum of
    :return: the minimum of the elements of the array
    """
    # min_val: int = tableau[0]

    # for i in range(1, len(tableau)):
    #     if tableau[i] < min_val:
    #         min_val = tableau[i]
    # return min_val

    # for elem in tableau: # O(n)
    #     if elem < min_val:
    #         min_val = elem
    # return min_val

    # tableau.sort()
    # return tableau[0]

    # return sorted(tableau)[0] # O(n*log(n))
    return reduce(lambda acc, value: value if value < acc else acc, tableau, tableau[0])


def max(tableau: list[int]) -> int:
    """
    Function that returns the maximum of the elements of the array
    :param tableau: the array to find the maximum of
    :return: the maximum of the elements of the array
    """
    return reduce(lambda acc, value: value if value > acc else acc, tableau, tableau[0])


def min_max(tableau: list[int]) -> tuple[int, int]:
    """
    Function that returns the minimum and maximum of the elements of the array
    :param tableau: the array to find the minimum and maximum of
    :return: the minimum and maximum of the elements of the array
    """
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

def variance(tableau: list[int]) -> float: # O(n^2)
    """
    Function that returns the variance of the elements of the array
    :param tableau: the array to find the variance of
    :return: the variance of the elements of the array
    """
    # mean = sum(tableau) / len(tableau)
    # sum_squared: list[float] = [(x-mean)**2 for x in tableau]
    # return sum(sum_squared) / len(tableau)

    # x_bar: float = average(tableau) 
    # sum_: float = 0.0               

    # for xi in tableau:            
    #     sum_ += (xi-x_bar)**2    
    
    # return sum_ / len(tableau)
    
    x_bar: float = average(tableau) 
    return sum(map(lambda x: (x-x_bar)**2, tableau)) / len(tableau)

def standard_deviation(tableau: list[int]) -> float:
    """
    Function that returns the standard deviation of the elements of the array
    The standard deviation is the square root of the variance.
    :param tableau: the array to find the standard deviation of
    :return: the standard deviation of the elements of the array
    """
    return variance(tableau)**(1/2)


def exist(tableau: list[int], valeur: int) -> bool:
    """
    Function that returns True if the value exists in the array
    :param tableau: the array to check if the value exists in
    :param valeur: the value to check if it exists in the array
    :return: True if the value exists in the array, False otherwise
    """
    # for x in tableau:
    #     if x == valeur:
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
    # if not is_list_of_numbers(arr):
    #     return []
    
    # sorted_list: list[int] = []
    # arr_copy: list[int] = arr.copy()
    # for _ in range(len(arr)):
    #     min_val = min(arr_copy)
    #     min_position = position(arr_copy, min_val)
    #     sorted_list.append(arr_copy.pop(min_position))
    # return sorted_list

    for i in range(len(arr)-1):
        for j in range(i+1, len(arr)):
            if arr[j] < arr[i]:
                arr[i], arr[j] = (arr[j], arr[i])
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
                arr[i], arr[j] = (arr[j], arr[i])
                # tmp: int = arr[i]
                # arr[i] = arr[j]
                # arr[j] = tmp
    return arr


def median(tableau: list[int]) -> int:
    """
    Function that returns the median of the elements of the array
    :param tableau: the array to find the median of
    :return: the median of the elements of the array
    """
    sorted_tab: list[int] = sort_ascending(tableau)
    mid: int = len(tableau) // 2
    return (
        sorted_tab[mid] 
        if len(tableau) % 2 == 1 
        else (sorted_tab[mid] + sorted_tab[mid-1]) / 2
    )