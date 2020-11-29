from flask import Blueprint, render_template, redirect, url_for
from periscope import db
from periscope.ballasting.forms import LimitsForm
from periscope.models import Ballasting

ballasting_blueprint = Blueprint('ballasting', __name__, template_folder='templates/ballasting')

@ballasting_blueprint.route('/ballasting', methods=['GET', 'POST'])
def ballasting():
    form = LimitsForm()

    if form.validate_on_submit():

        result = Ballasting.query \
            .with_entities(Ballasting.compass, Ballasting.mean_wa, Ballasting.seq, Ballasting.streamer) \
                .filter_by(streamer=form.streamer.data) \
                .order_by(Ballasting.seq.desc()) \
                .all()

        temp = []
        res = []
        max_seq = result[0][2]

        for seq in range(1, max_seq + 1):
            temp.append(seq)
            for b in range(0, 30):
                for r in result:
                    if r[0] == b and r[2] == seq:
                        temp.append(r[1])

            res.append(temp)
            temp = []

        return render_template('ballasting.html', form=form, result=res)
    return render_template('ballasting.html', form=form)
