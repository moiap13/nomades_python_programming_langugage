from string import ascii_lowercase, ascii_uppercase, digits, punctuation

from wtforms import Form
from wtforms.fields import StringField, EmailField, IntegerField, PasswordField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

def validate_password(form, field):
  data = field.data
  return True
  if len(data) < 8:
    raise ValidationError("Password must be at least 8 characters long")
  if not any([char in ascii_lowercase for char in data]):
    raise ValidationError("Password must contain at least one lower case")
  if not any([char in ascii_uppercase for char in data]):
    raise ValidationError("Password must contain at least one upper case")
  if not any([char in digits for char in data]):
    raise ValidationError("Password must contain at least one digit")
  if not any([char in punctuation for char in data]):
    raise ValidationError("Password must contain at least one special char")

class RegisterForm(Form):
  uid = StringField('Username', validators=[DataRequired(), Length(5)], render_kw={'placeholder': "Username"})
  firstname = StringField('Firstname', validators=[DataRequired(), Length(3)])
  lastname = StringField('Lastname', validators=[DataRequired(), Length(3)])
  email = EmailField('Email', validators=[DataRequired(), Email()])
  age = IntegerField('Age', validators=[DataRequired()])
  pwd = PasswordField('Password', validators=[DataRequired(), validate_password])
  pwd2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('pwd', 'PASSWORD MISMATCH')])

class LoginForm(Form):
  pass