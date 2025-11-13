def say_hello() -> None:
    """
    Function used to be imported and says hello !
    """
    print(f"Hello from callee.py!")


def say_hello_2() -> None:
    """
    Function used to be imported and says hello !
    """
    print(f"Hello 2 from callee.py!")


PI = 3.14

if __name__ == "__main__":
    print(f"random integer: {random.randint(1, 100)}")
    print("Hello World !")
