#TODO: WTForms: Create register and login from classes (look at flask/example/WTForms project)
from wtforms import Form
from wtforms.fields import StringField, EmailField, IntegerField, PasswordField
from wtforms.validators import DataRequired, Length, Email, EqualTo

def validate_password(form, field):
  return True
  data = field.data
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
  uid = StringField('Username', validators=[DataRequired(), Length(5)])
  firstname = StringField('Firstname', validators=[DataRequired(), Length(3)])
  lastname = StringField('Lastname', validators=[DataRequired(), Length(3)])
  email = EmailField('Email', validators=[DataRequired(), Email()])
  age = IntegerField('Age', validators=[DataRequired()])
  pwd = PasswordField("Password", validators=[DataRequired(), validate_password])
  pwd2 = PasswordField("Password", validators=[DataRequired(), EqualTo("pwd")])

class LoginForm(Form):
  uid = StringField('Username', validators=[DataRequired()])
  pwd = PasswordField("Password", validators=[DataRequired()])
