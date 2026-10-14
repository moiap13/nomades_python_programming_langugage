from string import ascii_lowercase, ascii_uppercase, digits, punctuation

from wtforms import Form, StringField, EmailField, PasswordField, FileField
from wtforms.validators import DataRequired, Length, Email, EqualTo, Optional, ValidationError

def validate_images_extensions(form, field):
  if field.data.content_type not in ("image/jpg", "image/jpeg", "image/png"):
    raise ValidationError("Only JPG and PNG image files supported")

def validate_password(form, field):
  if not any([char in ascii_lowercase for char in field.data]):
    raise ValidationError("Password must contain at least one lower case")
  if not any([char in ascii_uppercase for char in field.data]):
    raise ValidationError("Password must contain at least one upper case")
  if not any([char in digits for char in field.data]):
    raise ValidationError("Password must contain at least one digit")
  if not any([char in punctuation for char in field.data]):
    raise ValidationError("Password must contain at least one special char")
   

class RegisterForm(Form):
  firstname = StringField('Firstname', validators=[DataRequired(), Length(3, 20)], render_kw={"placeholder": "Firstname"})
  lastname = StringField('Lastname', validators=[DataRequired(), Length(3, 20)], render_kw={"placeholder": "Lastname"})
  uid = StringField('Username', validators=[DataRequired(), Length(5, 20)], render_kw={"placeholder": "Username"})
  email = EmailField('Email', validators=[DataRequired(), Email()], render_kw={"placeholder": "Email"})
  pp = FileField('Profile Picture', validators=[Optional(), validate_images_extensions], render_kw={"accept": "image/jpeg, image/png, image/jpg"})
  pwd = PasswordField("Password", validators=[DataRequired(), Length(8)], render_kw={"placeholder": "Password"})
  pwd2 = PasswordField("Repeat Password", validators=[DataRequired(), EqualTo("pwd", "PASSWORD MISMATCH")], render_kw={"placeholder": "Repeat Password"})
