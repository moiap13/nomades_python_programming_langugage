import random
import math

MAX_RANGE: int = 100
LIMIT_BRAVO: int = math.ceil(math.log2(MAX_RANGE)) # dychtomotic search number


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

    # 1. initial state
    user_number: int = int(input(f"Enter a number between (1 and {MAX_RANGE}): "))
    tries: int = 1 # 1 because we already ask the user once for a guess

    # 2. searching state
    while user_number != secret_number:
        if user_number > secret_number:
            # if the number entered is bigger than the secret number, print "too high"
            print("Too high")
        elif user_number < secret_number:
            # if the number entered is smaller than the secret number, print "too low"
            print("Too low")
        
        user_number: int = int(input(f"Enter a number between (1 and {MAX_RANGE}): "))
        tries += 1

    # 3. found state
    # if the number entered is equal to the secret number, print "You found the secret number", and the programs stop
    # (OPTIONAL): count the number of guesses and print it at the end
    # (OPTIONAL): print "Bravo" if the number of guesses is less than 7
    print(f"{'Bravo, y' if tries <= LIMIT_BRAVO else 'Y'}ou found the secret number in {tries} {'try' if tries == 1 else 'tries'}")

if __name__ == "__main__":
    # Run the game
    guess_number()
