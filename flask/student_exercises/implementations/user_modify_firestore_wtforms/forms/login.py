import string

from wtforms import Form
from wtforms.fields import StringField, PasswordField, EmailField, FileField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

def validate_password(form, field):
  if len(field.data) < 8:
    raise ValidationError("Password must be at least 8 characters long")
  if not any(c.isupper() for c in field.data):
    raise ValidationError("Password must contain at least one uppercase letter")
  if not any(c.islower() for c in field.data):
    raise ValidationError("Password must contain at least one lowercase letter")
  if not any(c.isdigit() for c in field.data):
    raise ValidationError("Password must contain at least one number")
  if not any(c in string.punctuation for c in field.data):
    raise ValidationError("Password must contain at least one special character")

  return field.data

def validate_pp(form, field):
  if field.data.content_type not in ["image/jpg", "image/jpeg", "image/png"]:
    raise ValidationError(f"Invalid file type {field.data.content_type} is not part of ['image/jpg', 'image/jpeg', 'image/png']")

  return field.data

class LoginForm(Form):
  uid = StringField('Username', validators=[DataRequired()], render_kw={'placeholder': "Username"})
  pwd = PasswordField("Password", validators=[DataRequired()], render_kw={'placeholder': "Password"})

class RegisterForm(Form):
  uid = StringField('Username', validators=[DataRequired(), Length(5, message="Username must be at least 5 characters long")], render_kw={'placeholder': "Username"})
  firstname = StringField('Firstname', validators=[DataRequired(), Length(3)], render_kw={'placeholder': "Firstname"})
  lastname = StringField('Lastname', validators=[DataRequired(), Length(3)], render_kw={'placeholder': "Lastname"})
  email = EmailField('Email', validators=[DataRequired(), Email()], render_kw={'placeholder': "Email"})
  # TODO: make pp optional
  pp = FileField('Profile Picture', validators=[DataRequired(), validate_pp], render_kw={'accept': "image/jpg, image/jpeg, image/png"})
  pwd = PasswordField('Password', validators=[DataRequired()], render_kw={'placeholder': "Password"})
  pwd2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('pwd', 'PASSWORD MISMATCH')], render_kw={'placeholder': "Repeat Password"})