import random
import math

MAX_RANGE: int = 1000

def guess_number():
    """
    Function that generates a random number between 1 and 100 and asks the user to guess it.
    :return: None
    """

    # Generate a random number between 1 and 100
    secret_number: int = random.randint(1, MAX_RANGE)
    # optimal tries is the dychotomic value for the given range
    optimal_tries: int = math.ceil(math.log2(MAX_RANGE))
    print(secret_number, optimal_tries)

    # to ask user to enter the number use the function input
    # convert the string to an integer using the int() function
    user_number: int = int(input(f"Please enter a number between (1 and {MAX_RANGE}): "))
    tries: int = 1

    # Exemple sans machine d'etat
    # found = False
    
    # while not found:
    #   # STATE: we did'nt found the number

    #   # dans la boucle les deux nombres ne sont pas pareils 
    #   #   -> l'utilisateur n'a pas trouvé le nombre secret
    #   if user_number > secret_number:
    #       print("Too high")
    #       user_number: int = int(input(f"Please enter a number between (1 and {MAX_RANGE}): "))
    #   elif user_number < secret_number:
    #       print("Too low")
    #       user_number: int = int(input(f"Please enter a number between (1 and {MAX_RANGE}): "))
    #   elif user_number == secret_number:
    #       print("You found the number")
    #       found = True        

    while user_number != secret_number:
      # STATE: we did'nt found the number

      # dans la boucle les deux nombres ne sont pas pareils 
      #   -> l'utilisateur n'a pas trouvé le nombre secret
      if user_number > secret_number:
          print("Too high")
      elif user_number < secret_number:
          print("Too low")
      
      user_number: int = int(input(f"Please enter a number between (1 and {MAX_RANGE}): "))
      tries += 1 # tries = tries + 1: on incrémente le compteur de 1
      
    # STATE: we found the number
    print(f"{'Bravo, y' if tries < optimal_tries else 'Y'}ou found the number in {tries} {'try' if tries == 1 else 'tries'}")

if __name__ == "__main__":
    # Run the game
    guess_number()
