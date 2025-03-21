import string
import random
import math

MIN_LENGTH_PASSWORD: int = 4

def generate_password(
    uppercase: bool, 
    lowercase: bool, 
    digits: bool, 
    specials_char: bool, 
    length: int,
    unique: bool = False,
    split_by: int = 0
) -> str:
  if not (uppercase or lowercase or digits or specials_char): 
    raise ValueError("Please select at least one population")
  
  if length < MIN_LENGTH_PASSWORD:
    raise ValueError(f"Please enter a password length greater or equal to {MIN_LENGTH_PASSWORD}")
  
  if split_by < 0:
    raise ValueError("split_by parameter must be positive")
  
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

  if unique and len(authorized_chars) < length:
    raise ValueError("When selecting unique password the length should be lower than the max population lenth")
  
  # password_l: list[str] = list(password) + random.choices(authorized_chars, k=(length - len(password)))
  # random.shuffle(password_l)

  while(len(password) < length):
    random_value = random.choice(authorized_chars)
    # while(unique and random_value in password):
    #   random_value = random.choice(authorized_chars)
    char_idx: int = authorized_chars.index(random_value)
    authorized_chars = authorized_chars[:char_idx] + authorized_chars[char_idx+1:]
    
    password += random_value
  
  password_l = list(password)
  random.shuffle(password_l)

  if split_by > 0:
    # "-".join(["".join(password_l[(i-1)*split_by: i*split_by]) for i in range(1, (math.ceil(length/split_by))+1)]
    password_chunks: list[str] = []
    for i in range(1, (math.ceil(length/split_by))+1):
      password_chunk: str = "".join(password_l[(i-1)*split_by: i*split_by])
      password_chunks.append(password_chunk)
    
    return "-".join(password_chunks)
  return "".join(password_l)

def main():
  print(generate_password(True, False, True, False, 20, True, 6))

if __name__ == '__main__':
    main()