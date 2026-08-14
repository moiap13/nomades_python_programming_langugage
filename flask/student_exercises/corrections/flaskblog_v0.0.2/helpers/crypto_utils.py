import hashlib

def hash_pwd(pwd: str, salt: str) -> str:
  h_pwd: str = hashlib.sha256((pwd+salt).encode()).hexdigest()
  return h_pwd
