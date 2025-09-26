# TODO: create the WTForm class ArticleAddForm to create the article form
# This form contains title: StringField and body: TextAreaField
# for the validators, title: DataRequired; body: DataRequired, Length max 500

from wtforms import Form
from wtforms.fields import StringField, TextAreaField
from wtforms.validators import DataRequired, Length


class ArticleAddForm(Form):
    title = StringField("Title", validators=[DataRequired()])
    body = TextAreaField("Body", validators=[DataRequired(), Length(max=500)])
