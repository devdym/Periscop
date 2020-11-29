from flask_wtf import FlaskForm
from wtforms import (SubmitField)


class CopyForm(FlaskForm):
    seal_logs = SubmitField('Copy Seal Logs')
    gunlink_logs = SubmitField('Copy GunLink Logs')
    tension_logs = SubmitField('Copy Tension Logs')
