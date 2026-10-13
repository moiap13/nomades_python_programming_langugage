import hashlib

def hash_pwd(pwd: str, salt: str) -> str:
  return hashlib.sha256((pwd+salt).encode()).hexdigest()