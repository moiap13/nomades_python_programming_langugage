import string
import random

def generate_password(
    uppercase: bool, 
    lowercase: bool, 
    digits: bool, 
    specials_char: bool, 
    length: int
) -> str:
  # test if the password legth greater or equal than 4
  if length < 4:
    return "Error: Length must be at least 4"
  
  # Generate a random password
  pwd: str = ""
  population: str = ""
  
  if uppercase:
    pwd += random.choice(string.ascii_uppercase)
    population += string.ascii_uppercase
  
  if lowercase:
    pwd += random.choice(string.ascii_lowercase)
    population += string.ascii_lowercase
  
  if digits:
    pwd += random.choice(string.digits)
    population += string.digits

  if specials_char:
    pwd += random.choice(string.punctuation)
    population += string.punctuation

  if len(pwd) == 0:
    return "Error: Please select at least one population"

  # for _ in range(length-len(pwd)):
  #   pwd += random.choice(population)
  # shuffled: list[str] = list(pwd)
  # random.shuffle(shuffled)
  # return "".join(shuffled)

  pwd_l: list[str] = list(pwd) + random.choices(population, k=length-len(pwd))
  random.shuffle(pwd_l)
  return "".join(pwd_l)


if __name__ == '__main__':
  print(generate_password(True, True, True, True, 122))