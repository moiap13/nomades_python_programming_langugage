from wtforms import Form, PasswordField
from wtforms.fields.html5 import EmailField
from wtforms.validators import email, DataRequired

class LoginForm(Form):
  email = EmailField("Email address CLASS", validators=[DataRequired(), email(message="Please enter a valid email address format")])
  pwd = PasswordField("Password", validators=[DataRequired()])