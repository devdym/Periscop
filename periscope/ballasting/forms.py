from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, BooleanField, SelectField, RadioField
from wtforms.validators import DataRequired

class LimitsForm(FlaskForm):
    streamer = SelectField(u'Streamer', choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6')], validators=[DataRequired()])
    min_wa = SelectField(u'min wa: ', choices=[(-7, '7'), (-6, '6'), (-5, '-5'), (-4, '-4'), (-3, '-3'), (-2, '-2')], default='-5', validators=[DataRequired()])
    max_wa = SelectField(u'max wa: ', choices=[(2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7')], default='5', validators=[DataRequired()])
    skip_h = SelectField(u'skip at head: ', choices=[('3', '3'), ('2', '2')], validators=[DataRequired()])
    skip_t = SelectField(u'skip at tail: ', choices=[('3', '3'), ('2', '2')], validators=[DataRequired()])
    submit = SubmitField('Apply')

