import string

from wtforms import Form
from wtforms.fields import (
    StringField,
    EmailField,
    IntegerField,
    PasswordField,
    FileField,
)
from wtforms.validators import DataRequired, Length, Email, NumberRange, EqualTo
from wtforms import ValidationError


def validate_password(form, field):
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
    if field.data.content_type not in ["image/jpeg", "image/jpg", "image/png"]:
        raise ValidationError("The file must be an image")


class RegisterForm(Form):
    uid = StringField("Username", validators=[DataRequired(), Length(min=5)])
    firstname = StringField("Firstname", validators=[DataRequired(), Length(min=2)])
    lastname = StringField("Lastname", validators=[DataRequired(), Length(min=2)])
    email = EmailField("Email", validators=[DataRequired(), Email()])
    age = IntegerField(
        "Age", validators=[DataRequired(), NumberRange(min=13, message="13 <= number")]
    )
    pp = FileField("Profile picture", validators=[DataRequired(), image_type])
    pwd = PasswordField("Password", validators=[DataRequired()])
    pwd2 = PasswordField(
        "Repeat password",
        validators=[DataRequired(), EqualTo("pwd", "Password mismatch")],
    )


class LoginForm(Form):
    uid = StringField("Username or Email", validators=[DataRequired(), Length(min=5)])
    pwd = PasswordField("Password", validators=[DataRequired()])
