from wtforms import Form, PasswordField, StringField, RadioField
from wtforms.fields.html5 import EmailField, DateField
from wtforms.validators import email, DataRequired

class LoginForm(Form):
  email = EmailField("Email address CLASS", validators=[DataRequired(), email(message="Please enter a valid email address format")])
  pwd = PasswordField("Password", validators=[DataRequired()])

# TODO: create the RegisterForm class with:
# - firstname, stringfield, [DataRequired] 
# - lastname, stringfield, [DataRequired] 
# - username, stringfield, [DataRequired] 
# - dob, DateField, [DataRequired]
# - BONUS gender, RadioField, [DataRequired], look at values parameter
# - email, EmailField, [DataRequired, email]
# - pwd, PasswordField, [DataRequired]
# - pwd2, PasswordField, [DataRequired, EqualTo("pwd")]