# WTForms: Create register and login from classes (look at flask/example/WTForms project)
from wtforms import Form
from wtforms.fields import StringField, TextAreaField, IntegerField
from wtforms.validators import DataRequired, Length, Email


class CreatePostForm(Form):
  title = StringField('Title', validators=[DataRequired(), Length(5)])
  body = TextAreaField('Body', validators=[DataRequired(), Length(min=-1, max=500)])
