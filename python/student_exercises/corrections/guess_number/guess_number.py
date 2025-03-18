import random
import math

MAX_NUMBER = 100

def guess_number():
    """
    Function that generates a random number between 1 and 100 and asks the user to guess it.
    :return: None
    """
    # for dychtomy optimal search, the formula is the following: log2(100)

    # Generate a random number between 1 and 100
    secret_number: int = random.randint(1, MAX_NUMBER)
    print(secret_number)

    user_num: int = int(input(f"Enter a number between 1 and {MAX_NUMBER}: "))
    tries: int = 1
    
    while user_num != secret_number:
        if user_num < secret_number:
            print("the guess number is higher")
        elif user_num > secret_number:
            print("the guess number is lower")
        user_num = int(input(f"Enter a number between 1 and {MAX_NUMBER}: "))
        tries += 1

    assert user_num == secret_number
    optimal_tries: int = math.ceil(math.log2(MAX_NUMBER))
    print(f"{'Bravo! ' if tries <= optimal_tries else ''}You have guessed the number in {tries} {'try' if tries==1 else 'tries'}")

if __name__ == '__main__':
    # Run the game
    guess_number()
