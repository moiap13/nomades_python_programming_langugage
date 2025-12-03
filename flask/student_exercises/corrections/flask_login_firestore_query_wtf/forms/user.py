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


class UserModifyForm(Form):
    uid = StringField("Username", validators=[DataRequired(), Length(min=5)])
    firstname = StringField("Firstname", validators=[DataRequired(), Length(min=2)])
    lastname = StringField("Lastname", validators=[DataRequired(), Length(min=2)])
    email = EmailField("Email", validators=[DataRequired(), Email()])
    age = IntegerField(
        "Age", validators=[DataRequired(), NumberRange(min=13, message="13 <= number")]
    )
    pp = FileField(
        "Profile picture",
        validators=[image_type],
        render_kw={"accept": "image/jpg, image/jpeg, image/png"},
    )
    old_pwd = PasswordField("Old password")
    new_pwd = PasswordField(
        "New password",
        validators=[validate_password],
    )
    new_pwd_2 = PasswordField(
        "Repeat new ypassword",
        validators=[EqualTo("new_pwd", "Password mismatch")],
    )
