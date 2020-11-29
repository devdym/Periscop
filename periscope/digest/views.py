from flask import Blueprint, render_template, redirect, url_for
from periscope.digest.forms import CopyForm

digest_blueprint = Blueprint('digest', __name__, template_folder='templates/digest')


@digest_blueprint.route('/digest', methods=['GET', 'POST'])
def digest():
    form = CopyForm()

    if form.validate_on_submit():
        name = form.errors_only.data
        return redirect(url_for('digest.digest'))

    return render_template('digest.html', form=form)
