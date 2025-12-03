import string

from wtforms import ValidationError


def validate_password(form, field):
    # TODO: Remove return None when deploying
    return None
    if len(field.data) < 8:
        raise ValidationError("The password must be at least 8 chars")
    if not any([c.isupper() for c in field.data]):
        raise ValidationError("The password needs at least one upper case char")
    if not any([c.islower() for c in field.data]):
        raise ValidationError("The password needs at least one lower case char")
    if not any([c.isdigit() for c in field.data]):
        raise ValidationError("The password needs at least one digit char")
    if not any([(c in string.punctuation) for c in field.data]):
        raise ValidationError("The password needs at least one special char")


def image_type(form, field):
    if field.data and field.data.content_type not in [
        "image/jpeg",
        "image/jpg",
        "image/png",
    ]:
        raise ValidationError("The file must be an image")
