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
    pp_filename: str = "",
    geo_position: dict[str, float] = {}
  ) -> None:
    self.firestore_id = firestore_id
    self.uid = uid
    self.email = email
    self.firstname = firstname
    self.lastname = lastname
    self.pwd = pwd
    self.salt = salt
    self.pp_filename = pp_filename
    self.geo_position = geo_position

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
      pp_filename=user_dict["pp_filename"] if "pp_filename" in user_dict else "",
      geo_position=user_dict["geo_position"] if "geo_position" in user_dict else {}
    )

  def to_dict(self, include_id: bool = False, include_pp: bool = False, include_pwd: bool = False, include_geo: bool = False) -> dict[str, str]:
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
    if include_geo:
      ret.update({ "geo_position": self.geo_position })

    return ret

  def get_fullname(self) -> str:
    return f"{self.firstname} {self.lastname}"

  def __eq__(self, other: Any): # other can be either str or User object
    if not (isinstance(other, User) or isinstance(other, str)): 
      return False

    if type(other) == str:
      return self.firestore_id == other
    return self.firestore_id == other.firestore_id