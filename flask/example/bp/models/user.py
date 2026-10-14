class User:
  def __init__(
    self, 
    firestore_id: str = "",
    firstname: str = "",
    lastname: str = "",
    email: str = "",
    uid: str = "",
    salt: str = "",
    pwd: str = "",
    pp_filename: str = ""
  ):
    self.firestore_id = firestore_id
    self.firstname = firstname
    self.lastname = lastname
    self.email = email
    self.uid = uid
    self.salt = salt
    self.pwd = pwd
    self.pp_filename = pp_filename

  def to_dict(self, include_id: bool = False, include_pwd: bool = False) -> dict[str, str]:
    return {
      "firstname": self.firstname,
      "lastname": self.lastname,
      "email": self.email,
      "uid": self.uid,
    } | (
      {"firestore_id": self.firestore_id} if include_id else {}
    ) | (
      {
        "salt": self.salt, 
        "pwd": self.pwd
      } if include_pwd else {}
    ) | (
      {"pp_filename": self.pp_filename} if self.pp_filename != None else {}
    )

  def get_fullname(self) -> str:
    return f"{self.firstname} {self.lastname}"

  def get_uiavatars_url(self) -> str:
    return f"https://ui-avatars.com/api/?name={self.firstname}+{self.lastname}&background=random"

  @staticmethod
  def from_dict(user: dict[str, str]) -> "User":
   return User(
      firestore_id=user.get("firestore_id", ""),
      firstname=user.get("firstname", ""),
      lastname=user.get("lastname", ""),
      email=user.get("email", ""),
      uid=user.get("uid", ""),
      salt=user.get("salt", ""),
      pwd=user.get("pwd", ""),
      pp_filename=user.get("pp_filename", "")
  )