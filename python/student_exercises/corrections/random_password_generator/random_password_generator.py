import string
import random

MIN_LENGTH_PASSWORD: int = 4

def generate_password(
    uppercase: bool, 
    lowercase: bool, 
    digits: bool, 
    specials_char: bool, 
    length: int
) -> str:
  if not (uppercase or lowercase or digits or specials_char):
    return "Please select at least one population"
  
  # TODO: test if the password legth greater or equal than 4
  if length < MIN_LENGTH_PASSWORD:
    return f"Please enter a password length greater or equal to {MIN_LENGTH_PASSWORD}"
  
  password: str = ''
  authorized_chars: str = ''

  if uppercase:
    password += random.choice(string.ascii_uppercase)
    authorized_chars += string.ascii_uppercase 

  if lowercase:
    password += random.choice(string.ascii_lowercase)
    authorized_chars += string.ascii_lowercase 

  if digits:
    password += random.choice(string.digits)
    authorized_chars += string.digits 

  if specials_char:
    password += random.choice(string.punctuation)
    authorized_chars += string.punctuation 

  print(password, authorized_chars)
  return "None"

if __name__ == '__main__':
  print(generate_password(True, False, True, False, 5))