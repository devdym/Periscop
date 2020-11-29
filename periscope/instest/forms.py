from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField, RadioField
from wtforms.fields.html5 import DateField


class LimitsForm(FlaskForm):
    date_ = DateField('Date')
    submit = SubmitField('Apply')