from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, BooleanField, RadioField


class LimitsForm(FlaskForm):
    value = RadioField('value', choices=[('week', 'week'), ('month', 'month'), ('project', 'project')])
    submit = SubmitField('Apply')
