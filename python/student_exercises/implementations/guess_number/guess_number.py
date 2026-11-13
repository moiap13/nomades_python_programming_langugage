import random
import math

MAX_RANGE: int = 100


def guess_number():
    """
    Function that generates a random number between 1 and 100 and asks the user to guess it.
    :return: None
    """

    # Generate a random number between 1 and 100
    secret_number: int = random.randint(1, MAX_RANGE)
    print(secret_number)

    # to ask user to enter the number use the function input
    # convert the string to an integer using the int() function
    # if the number entered is bigger than the secret number, print "too high"
    # if the number entered is smaller than the secret number, print "too low"
    # if the number entered is equal to the secret number, print "You found the secret number", and the programs stop
    # (OPTIONAL): count the number of guesses and print it at the end
    # (OPTIONAL): print "Bravo" if the number of guesses is less than 7
    print("bravo")


if __name__ == "__main__":
    # Run the game
    guess_number()
