from wtforms import Form, StringField, TextAreaField
from wtforms.validators import Length, DataRequired

class CreatePostForm(Form):
  title = StringField('Title', validators=[DataRequired(), Length(5)], render_kw={"placeholder": "Title"})
  body = TextAreaField('Body', validators=[DataRequired(), Length(min=-1, max=15000)], render_kw={"placeholder": "Body"})