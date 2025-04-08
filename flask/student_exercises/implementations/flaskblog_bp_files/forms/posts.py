from wtforms import Form
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired

class PostCreateForm(Form):
  title = StringField("Post title", validators=[DataRequired()])
  body = TextAreaField("Body", validators=[DataRequired()], render_kw={"rows": 10 })