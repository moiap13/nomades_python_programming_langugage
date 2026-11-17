import random
import math # dychotomique

MAX_RANGE: int = 100

def guess_number():
    """
    Function that generates a random number between 1 and 100 and asks the user to guess it.
    :return: None
    """
    # initialization state
    # Generate a random number between 1 and 100
    secret_number: int = random.randint(1, MAX_RANGE)
    print(secret_number)
    user_number: int = int(input(f"Enter a number between (1 and {MAX_RANGE}): "))
    tries: int = 1
    optimal_tries: int = math.ceil(math.log2(MAX_RANGE))

    # Guessing state
    while user_number != secret_number:
        if user_number > secret_number:
            print("to high")
        elif user_number < secret_number:
            print("to low")

        user_number: int = int(input(f"Enter a number between (1 and {MAX_RANGE}): "))
        tries += 1
    
    # Winning state         
    print(
        f"{'Bravo, y' if tries < optimal_tries else 'Y'}ou "
        f"found the secret number in {tries} "
        f"{'try' if tries == 1 else 'tries'}"
    )

    # to ask user to enter the number use the function input
    # convert the string to an integer using the int() function
    # if the number entered is bigger than the secret number, print "too high"
    # if the number entered is smaller than the secret number, print "too low"
    # if the number entered is equal to the secret number, print "You found the secret number", and the programs stop
    # (OPTIONAL): count the number of guesses and print it at the end
    # (OPTIONAL): print "Bravo" if the number of guesses is less than 7


if __name__ == "__main__":
    # Run the game
    guess_number()
