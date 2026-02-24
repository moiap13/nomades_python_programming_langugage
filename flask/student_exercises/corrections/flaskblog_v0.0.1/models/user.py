class User:
    def __init__(
        self,
        id: str,
        firstname: str,
        lastname: str,
        email: str,
        uid: str,
        salt: str,
        password: str,
        avatar: str,
    ) -> None:
        self.id = id
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.uid = uid
        self.salt = salt
        self.password = password
        self.avatar = avatar

    def __repr__(self) -> str:
        return f"User({self.uid}, {self.email})"

    def __str__(self) -> str:
        return self.__repr__()

    @staticmethod
    def from_dict(user_data: dict[str, str]) -> "User":
        return User(
            id=user_data.get("id", ""),
            firstname=user_data.get("firstname", ""),
            lastname=user_data.get("lastname", ""),
            email=user_data.get("email", ""),
            uid=user_data.get("uid", ""),
            salt=user_data.get("salt", ""),
            password=user_data.get("password", ""),
            avatar=user_data.get("avatar", ""),
        )

    def to_list(self, include_password=False) -> list[str]:
        return [
            self.firstname,
            self.lastname,
            self.email,
            self.uid,
            self.avatar,
        ] + ([self.salt, self.password] if include_password else [])

    def to_dict(
        self, include_password=False, include_id: bool = False
    ) -> dict[str, str]:
        return (
            {
                "firstname": self.firstname,
                "lastname": self.lastname,
                "email": self.email,
                "uid": self.uid,
                "avatar": self.avatar,
            }
            | (
                {"salt": self.salt, "password": self.password}
                if include_password
                else {}
            )
            | ({"id": self.id} if include_id else {})
        )

    def get_fullname(self) -> str:
        return f"{self.firstname} {self.lastname}"

    def get_ui_avatar_url(self) -> str:
        return f"https://ui-avatars.com/api/?name={self.firstname}+{self.lastname}&background=random"
