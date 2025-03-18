def say_hello(): # doc-string
    """
    Function that says hello
    """
    print(f"Hello from callee.py!")

def say_hello_2(): # doc-string
    """
    Another function that says hello
    """
    print(f"Hello from callee.py 2!")

  
if __name__ == "__main__":
    print("callee executed directly")