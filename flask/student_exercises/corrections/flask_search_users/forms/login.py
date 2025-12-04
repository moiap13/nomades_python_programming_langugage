from wtforms import Form
from wtforms.fields import (
    StringField,
    EmailField,
    IntegerField,
    PasswordField,
    FileField,
)
from wtforms.validators import DataRequired, Length, Email, NumberRange, EqualTo

from .custom_validators import image_type, validate_password


class RegisterForm(Form):
    uid = StringField("Username", validators=[DataRequired(), Length(min=5)])
    firstname = StringField("Firstname", validators=[DataRequired(), Length(min=2)])
    lastname = StringField("Lastname", validators=[DataRequired(), Length(min=2)])
    email = EmailField("Email", validators=[DataRequired(), Email()])
    age = IntegerField(
        "Age", validators=[DataRequired(), NumberRange(min=13, message="13 <= number")]
    )
    pp = FileField("Profile picture", validators=[image_type])
    pwd = PasswordField("Password", validators=[DataRequired(), validate_password])
    pwd2 = PasswordField(
        "Repeat password",
        validators=[DataRequired(), EqualTo("pwd", "Password mismatch")],
    )


class LoginForm(Form):
    uid = StringField("Username or Email", validators=[DataRequired(), Length(min=5)])
    pwd = PasswordField("Password", validators=[DataRequired()])
