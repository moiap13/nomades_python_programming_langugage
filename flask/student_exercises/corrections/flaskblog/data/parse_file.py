import json
import random
import hashlib

with open("users.json") as json_users:
    users: list[dict[str, int | str | dict[str, str]]] = json.load(json_users)
    for user in users:
        user["firstname"] = user["name"].split(" ")[0]
        user["lastname"] = "".join(user["name"].split(" ")[1:])
        user["age"] = random.randint(18, 100)
        user["salt"] = "AAAAAAAAAA"
        user["pwd"] = hashlib.sha512(
            ("password" + user["salt"]).encode("utf-8")
        ).hexdigest()
        user.pop("name")

with open("users.json", "w") as json_users:
    json.dump(users, json_users, indent=4)
