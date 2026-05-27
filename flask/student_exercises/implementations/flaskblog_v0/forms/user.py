# WTForms: Create register and login from classes (look at flask/example/WTForms project)
from wtforms import Form
from wtforms.fields import StringField, EmailField, IntegerField
from wtforms.validators import DataRequired, Length, Email


class UserModifyForm(Form):
  uid = StringField('Username', validators=[DataRequired(), Length(5)])
  firstname = StringField('Firstname', validators=[DataRequired(), Length(3)])
  lastname = StringField('Lastname', validators=[DataRequired(), Length(3)])
  email = EmailField('Email', validators=[DataRequired(), Email()])
  age = IntegerField('Age', validators=[DataRequired()])
