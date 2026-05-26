import os

class User:
  def __init__(
      self,
      id: str = '',
      uid: str = '',
      firstname: str = '',
      lastname: str = '',
      email: str = '',
      age: int = -1,
      pp_filename: str = '',
      pwd: str = '',
      salt: str = ''
  ) -> None:
    self.id = id
    self.uid = uid
    self.firstname = firstname
    self.lastname = lastname
    self.email = email
    self.age = age
    self.pp_filename = pp_filename
    self.pwd = pwd
    self.salt = salt

  def to_dict(self: "User") -> dict[str, str | int]:
    return {
      "uid": self.uid,
      "firstname": self.firstname,
      "lastname": self.lastname,
      "email": self.email,
      "age": self.age,
      "pwd": self.pwd,
      "salt": self.salt,
      'pp_filename': self.pp_filename
    }

  @staticmethod
  def from_dict(source: dict[str, str | int]) -> "User":
    return User(
      source.get("id", ""),
      source.get("uid", ""),
      source.get("firstname", ""),
      source.get("lastname", ""),
      source.get("email", ""),
      source.get("age", -1),
      source.get("pp_filename", ""),
      source.get("pwd", ""),
      source.get("salt", "")
    )
  
  def pp_exits(self, pp_dir: str) -> bool:
    user_pp_filename = os.path.join(
      pp_dir, 
      self.pp_filename if self.pp_filename != '' else 'UNKNOWN'
    )
    return os.path.exists(user_pp_filename)

  def get_pp_ui_avatars_src(self) -> str:
    return f"https://eu.ui-avatars.com/api/?name={self.firstname}+{self.lastname}&background=random"

