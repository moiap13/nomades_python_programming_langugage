# WTForms: Create register and login from classes (look at flask/example/WTForms project)
from wtforms import Form
from wtforms.fields import StringField, EmailField, IntegerField, PasswordField, FileField
from wtforms.validators import DataRequired, Length, Email, EqualTo

from .custom_validators import validate_password, validate_image

class RegisterForm(Form):
  uid = StringField('Username', validators=[DataRequired(), Length(5)])
  firstname = StringField('Firstname', validators=[DataRequired(), Length(3)])
  lastname = StringField('Lastname', validators=[DataRequired(), Length(3)])
  email = EmailField('Email', validators=[DataRequired(), Email()])
  age = IntegerField('Age', validators=[DataRequired()])
  pp = FileField('Profile Picture', validators=[DataRequired(), validate_image])
  pwd = PasswordField("Password", validators=[DataRequired(), validate_password])
  pwd2 = PasswordField("Password", validators=[DataRequired(), EqualTo("pwd")])

class LoginForm(Form):
  uid = StringField('Username', validators=[DataRequired()])
  pwd = PasswordField("Password", validators=[DataRequired()])
