from datetime import date
from flask_wtf import FlaskForm
from wtforms import FloatField, SubmitField
from wtforms.fields.html5 import DateField


class LimitsForm(FlaskForm):
    dt = DateField('Date', format='%Y-%m-%d', default=date.today())
    min_v_bank_a = FloatField(label=u'Min bank A: ', default='4.2')
    min_v_bank_b = FloatField(label=u'Min bank B: ', default='6.2')
    submit = SubmitField('Apply')
