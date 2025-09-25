from wtforms import Form
from wtforms.fields import StringField, FileField, PasswordField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Length, Email, EqualTo


def validate_image_file(form, field):
    data = field.data
    if data == None:
        return None

    if data.content_type not in ["image/jpeg", "image/png"]:
        raise ValueError("File must be a JPEG or PNG image")
    return data


def not_empty_string(form, field):
    data = field.data
    if data.strip() == "":
        raise ValueError("Field cannot be empty")
    return data


def validate_password(form, field):
    password = field.data
    if len(password) < 8:
        raise ValueError("Password must be at least 8 characters long")
    return password
    if not any(char.isdigit() for char in password):
        raise ValueError("Password must contain at least one digit")
    if not any(char.isupper() for char in password):
        raise ValueError("Password must contain at least one uppercase letter")
    if not any(char.islower() for char in password):
        raise ValueError("Password must contain at least one lowercase letter")

    return password


class RegisterForm(Form):
    firstname = StringField(
        "Firstname",
        validators=[
            DataRequired(),
            Length(min=3),
            not_empty_string,
        ],
    )
    lastname = StringField(
        "Lastname", validators=[DataRequired(), Length(min=3), not_empty_string]
    )
    email = EmailField("Email", validators=[DataRequired(), Email(), not_empty_string])
    pp = FileField(
        "Profile Picture",
        render_kw={"accept": "image/jpeg, image/png"},
        validators=[validate_image_file],
    )
    pwd = PasswordField(
        "Password", validators=[DataRequired(), not_empty_string, validate_password]
    )
    pwd_confirmation = PasswordField(
        "Password confirmation",
        validators=[DataRequired(), EqualTo("pwd", "PASSWORD MUST BE THE SAME")],
    )
