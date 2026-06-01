from wtforms import Form, SelectField, SelectMultipleField
from wtforms.validators import DataRequired

from .custom_validators import date_before

class AnalysisForm(Form):
  start_date = SelectField('Start Date', choices=[], validators=[DataRequired(), date_before])
  end_date = SelectField('End Date', choices=[], validators=[DataRequired(), date_before])
  authors = SelectMultipleField('Authors', choices=[], validators=[DataRequired()])