from wtforms import (
    Form,
    StringField,
    EmailField,
    FileField,
    PasswordField,
    ValidationError,
)
from wtforms.validators import Length, DataRequired, Email, EqualTo


def validate_password(form, field):
    import string

    if len(field.data) < 8:
        raise ValidationError("Password must be at least 8 characters long")

    if not any([char in string.ascii_uppercase for char in field.data]):
        raise ValidationError("Password must contain at least one uppercase letter")

    if not any([char in string.ascii_lowercase for char in field.data]):
        raise ValidationError("Password must contain at least one lowercase letter")

    if not any([char in string.digits for char in field.data]):
        raise ValidationError("Password must contain at least one digit")

    if not any([char in string.punctuation for char in field.data]):
        raise ValidationError("Password must contain at least one special character")


def file_type_image(form, field):
    if field.data and field.data.content_type not in [
        "image/jpeg",
        "image/jpg",
        "image/png",
    ]:
        raise ValidationError("Please provide an image")


class RegisterForm(Form):
    uid = StringField(
        "Username",
        validators=[DataRequired(), Length(5, 8)],
        render_kw={"placeholder": "Username"},
    )
    firstname = StringField(
        "Firstname", validators=[DataRequired()], render_kw={"placeholder": "Firstname"}
    )
    lastname = StringField(
        "Lastname", validators=[DataRequired()], render_kw={"placeholder": "Lastname"}
    )
    email = EmailField(
        "Email",
        validators=[DataRequired(), Email()],
        render_kw={"placeholder": "Email"},
    )
    avatar = FileField(
        "Avatar",
        validators=[file_type_image],
        render_kw={"accept": "image/jpg, image/jpeg, image/png"},
    )
    pwd = PasswordField(
        "Password",
        validators=[DataRequired(), validate_password],
        render_kw={"placeholder": "Password"},
    )
    pwd2 = PasswordField(
        "Repeat password",
        validators=[DataRequired(), EqualTo("pwd", message="PASWWORD MISMATCH")],
        render_kw={"placeholder": "Repeat password"},
    )


class LoginForm(Form):
    pass
