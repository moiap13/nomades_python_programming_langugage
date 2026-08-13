from typing import Any


class User:
  def __init__(
    self, 
    uid: str, 
    email: str, 
    firstname: str, 
    lastname: str, 
    firestore_id: str = "", 
    pwd: str = "", 
    salt: str = "", 
    pp_filename: str = ""
  ) -> None:
    self.firestore_id = firestore_id
    self.uid = uid
    self.email = email
    self.firstname = firstname
    self.lastname = lastname
    self.pwd = pwd
    self.salt = salt
    self.pp_filename = pp_filename

  @staticmethod
  def from_dict(user_dict: dict[str, Any]) -> "User":
    return User(
      uid=user_dict["uid"],
      email=user_dict["email"],
      firstname=user_dict["firstname"],
      lastname=user_dict["lastname"],
      firestore_id=user_dict["firestore_id"] if "firestore_id" in user_dict else "",
      pwd=user_dict["pwd"] if "pwd" in user_dict else "",
      salt=user_dict["salt"] if "salt" in user_dict else "",
      pp_filename=user_dict["pp_filename"] if "pp_filename" in user_dict else ""
    )

  def to_dict(self, include_id: bool = False, include_pp: bool = False, include_pwd: bool = False) -> dict[str, str]:
    ret: dict[str, str] = { 
      "uid": self.uid,
      "email": self.email,
      "firstname": self.firstname,
      "lastname": self.lastname,
    } 

    if include_id:
      ret.update({ "firestore_id": self.firestore_id })
    if include_pwd:
      ret.update({ "pwd": self.pwd, "salt": self.salt })
    if include_pp and self.pp_filename != None:
      ret.update({ "pp_filename": self.pp_filename })

    return ret

  def get_fullname(self) -> str:
    return f"{self.firstname} {self.lastname}"