class User:
    def __init__(
        self,
        uid: str = "",
        firstname: str = "",
        lastname: str = "",
        email: str = "",
        password: str = "",
        salt: str = "",
        pp_filename: str = "",
    ):
        self.uid = uid
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.password = password
        self.salt = salt
        self.pp_filename = pp_filename

    @staticmethod
    def from_dict(source: dict[str, str]) -> "User":
        """
        Create a User object from a dictionary

        Args:
            source (dict[str, str]): The dictionary to create the User object from

        Returns:
            User: The created User object
        """
        return User(
            uid=source.get("uid", ""),
            firstname=source.get("firstname", ""),
            lastname=source.get("lastname", ""),
            email=source.get("email", ""),
            password=source.get("password", ""),
            salt=source.get("salt", ""),
            pp_filename=source.get("pp_filename", ""),
        )

    def to_dict(self) -> dict[str, str]:
        """
        Convert the User object to a dictionary

        Returns:
            dict[str, str]: The dictionary representation of the User object
        """
        return {
            "firstname": self.firstname,
            "lastname": self.lastname,
            "email": self.email,
            "password": self.password,
            "salt": self.salt,
            "pp_filename": self.pp_filename,
        }

    def __repr__(self):
        return f"""City(\
              name={self.name},
              country={self.country},
              population={self.population},
              capital={self.capital},
              regions={self.regions}
          )"""

    def __str__(self):
        return self.__repr__()

    def full_name(self) -> str:
        return f"{self.firstname} {self.lastname}"
