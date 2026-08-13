# Create PostCreationForm
# This form should contain the following fields:
# - title: StringField
# - body: TextAreaField
from wtforms import Form
from wtforms.fields import StringField, TextAreaField
from wtforms.validators import DataRequired, Length

class PostCreationForm(Form):
    title = StringField('Title', validators=[DataRequired(), Length(5)], render_kw={"placeholder": "Title"})
    body = TextAreaField('Body', validators=[DataRequired(), Length(min=-1, max=1500)], render_kw={"placeholder": "Body"})