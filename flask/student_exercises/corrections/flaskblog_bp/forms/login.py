from wtforms import Form, PasswordField, StringField, RadioField, ValidationError
from wtforms.fields.html5 import EmailField, DateField
from wtforms.validators import email, DataRequired, Length, EqualTo

def password_verification(form, field):
  pwd = field.data
  if len(pwd) < 8:
    raise ValidationError("Password must be at least 8 characters long")
  if "'" not in pwd:
    raise ValidationError("Password must contain at least one apostrophe")
  

class LoginForm(Form):
  email = EmailField("Email address CLASS", validators=[DataRequired(), email(message="Please enter a valid email address format")])
  pwd = PasswordField("Password", validators=[DataRequired()])

# create the RegisterForm class with:
# - firstname, stringfield, [DataRequired] 
# - lastname, stringfield, [DataRequired] 
# - username, stringfield, [DataRequired] 
# - dob, DateField, [DataRequired]
# - BONUS gender, RadioField, [DataRequired], look at values parameter
# - email, EmailField, [DataRequired, email]
# - pwd, PasswordField, [DataRequired]
# - pwd2, PasswordField, [DataRequired, EqualTo("pwd")]

class RegisterForm(Form):
  firstname = StringField("Firstname", validators=[DataRequired(), Length(min=3, max=10)])
  lastname = StringField("Lastname", validators=[DataRequired(), Length(min=3, max=10)])
  username = StringField("Username", validators=[DataRequired(), Length(min=5, max=10)])
  dob = DateField("Date of birth", validators=[DataRequired()])
  email = EmailField("Email address CLASS", validators=[DataRequired(), email(message="Please enter a valid email address format")])
  gender = RadioField("Gender", validators=[DataRequired()], choices=[("female", "female"), ("male", "male")])
  pwd = PasswordField("Password", validators=[DataRequired(), password_verification])
  pwd2 = PasswordField("Repeat password", validators=[EqualTo("pwd")]) 