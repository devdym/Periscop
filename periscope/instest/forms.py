from datetime import date
from flask_wtf import FlaskForm
from wtforms import SubmitField
from wtforms.fields.html5 import DateField


class LimitsForm(FlaskForm):
    date_ = DateField('Date', format='%Y-%m-%d', default=date.today())
    submit = SubmitField('Apply')