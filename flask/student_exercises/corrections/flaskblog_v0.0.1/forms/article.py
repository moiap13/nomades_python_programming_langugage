from wtforms import (
    Form,
    StringField,
    TextAreaField,
)
from wtforms.validators import Length, DataRequired


# TODO (1): Create the article WTForm class
# thsi class contains:
# - title(StringField): DataRequired(), Length(min=5, max=20)
# - body(TextAreaField): DataRequired(), Length(min=5, max=3000)
class AddArticleForm(Form):
    title = StringField()
    body = TextAreaField()
