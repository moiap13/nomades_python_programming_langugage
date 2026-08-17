from wtforms import Form
from wtforms.fields import StringField, PasswordField, EmailField, FileField
from wtforms.validators import DataRequired, Length, Email, EqualTo, Optional

from .custom_validators import validate_pp

class LoginForm(Form):
  uid = StringField('Username', validators=[DataRequired()], render_kw={'placeholder': "Username"})
  pwd = PasswordField("Password", validators=[DataRequired()], render_kw={'placeholder': "Password"})

class RegisterForm(Form):
  uid = StringField('Username', validators=[DataRequired(), Length(5, message="Username must be at least 5 characters long")], render_kw={'placeholder': "Username"})
  firstname = StringField('Firstname', validators=[DataRequired(), Length(3)], render_kw={'placeholder': "Firstname"})
  lastname = StringField('Lastname', validators=[DataRequired(), Length(3)], render_kw={'placeholder': "Lastname"})
  email = EmailField('Email', validators=[DataRequired(), Email()], render_kw={'placeholder': "Email"})
  # make pp optional
  pp = FileField('Profile Picture', validators=[Optional(), validate_pp], render_kw={'accept': "image/jpg, image/jpeg, image/png"})
  pwd = PasswordField('Password', validators=[DataRequired()], render_kw={'placeholder': "Password"})
  pwd2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('pwd', 'PASSWORD MISMATCH')], render_kw={'placeholder': "Repeat Password"})