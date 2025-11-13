import string
import random


def generate_password(
    uppercase: bool, lowercase: bool, digits: bool, specials_char: bool, length: int
) -> str:
    if length < 4:
        return "Error: lenght must be >= 4"

    password: str = ""
    allowed_chars: list[str] = []
    checked: bool = False

    if uppercase:
        password += random.choice(string.ascii_uppercase)
        allowed_chars += [string.ascii_uppercase]
        checked = True

    if lowercase:
        password += random.choice(string.ascii_lowercase)
        allowed_chars += [string.ascii_lowercase]
        checked = True

    if digits:
        password += random.choice(string.digits)
        allowed_chars += [string.digits]
        checked = True

    if specials_char:
        password += random.choice(string.punctuation)
        allowed_chars += [string.punctuation]
        checked = True

    # if not checked:
    if len(password) == 0:
        return "Error: Please select at least one population"

    for _ in range(length - len(password)):
        password += random.choice(
            allowed_chars[random.randint(1, len(allowed_chars)) - 1]
        )

    l_password: list[str] = list(password)
    random.shuffle(l_password)
    return "".join(l_password)


if __name__ == "__main__":
    print(generate_password(True, True, True, True, 1))
