import string
import random

def generate_password(
    uppercase: bool, 
    lowercase: bool, 
    digits: bool, 
    specials_char: bool, 
    length: int
) -> str:
  if length < 4:
    return "Error: password length should be at least 4"
  
  pwd: str = ""
  available_chars: str = ""

  if uppercase:
    pwd += random.choice(string.ascii_uppercase)
    available_chars += string.ascii_uppercase

  if lowercase:
    pwd += random.choice(string.ascii_lowercase)
    available_chars += string.ascii_lowercase

  if digits:
    pwd += random.choice(string.digits)
    available_chars += string.digits

  if specials_char:
    pwd += random.choice(string.punctuation)
    available_chars += string.punctuation

  # if len(pwd) == 0:
  if pwd == "":
    return "Error: Please select at least one population"

  remaining_chars: list[str] = random.choices(available_chars, k=length-len(pwd))
  pwd_l: list[str] = list(pwd) + remaining_chars

  random.shuffle(pwd_l)

  return "".join(pwd_l)

if __name__ == '__main__':
  print(generate_password(True, True, True, False, 8))