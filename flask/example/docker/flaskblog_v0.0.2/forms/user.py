from wtforms import FileField, Form
from wtforms.fields import StringField, EmailField
from wtforms.validators import DataRequired, Length, Email, Optional

from .custom_validators import validate_pp

# Create the UserModifyForm class
class UserModifyForm(Form):
  uid = StringField('Username', validators=[DataRequired(), Length(5, message="Username must be at least 5 characters long")], render_kw={'placeholder': "Username"})
  firstname = StringField('Firstname', validators=[DataRequired(), Length(3)], render_kw={'placeholder': "Firstname"})
  lastname = StringField('Lastname', validators=[DataRequired(), Length(3)], render_kw={'placeholder': "Lastname"})
  email = EmailField('Email', validators=[DataRequired(), Email()], render_kw={'placeholder': "Email"})
  # Allow to modify the profile picture
  pp = FileField('Profile Picture', validators=[Optional(), validate_pp], render_kw={'accept': "image/jpg, image/jpeg, image/png"})
