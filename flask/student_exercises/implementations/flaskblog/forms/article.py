from wtforms import Form
from wtforms.fields import StringField, TextAreaField
from wtforms.validators import DataRequired, Length


class AddArticleForm(Form):
    title = StringField("Title", validators=[DataRequired(), Length(min=5, max=20)])
    body = TextAreaField("Body", validators=[DataRequired(), Length(min=5, max=300)])
