def comp_numbers(num1: int, num2: int) -> tuple[int, int]:
    """
    Function that compute both sum and difference for two numbers 
    
    Args:
        - num1(int): the first number
        - num2(int): the second number
    Retrun:
        - s(int): the sum
        - d(int): the difference
    """
    sum_: int = num1 + num2
    return sum_, num1 - num2

print(comp_numbers(5, 4))