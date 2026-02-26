from wtforms import (
    Form,
    StringField,
    TextAreaField,
)
from wtforms.validators import Length, DataRequired


# Create the article WTForm class
# thsi class contains:
# - title(StringField): DataRequired(), Length(min=5, max=20)
# - body(TextAreaField): DataRequired(), Length(min=5, max=3000)
class AddArticleForm(Form):
    title = StringField(
        "Title",
        validators=[DataRequired(), Length(5, 20)],
        render_kw={"placeholder": "Title"},
    )
    body = TextAreaField(
        "Body",
        validators=[DataRequired(), Length(5, 3000)],
        render_kw={"placeholder": "Body"},
    )
