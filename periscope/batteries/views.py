from flask import Blueprint, render_template
from periscope.batteries.forms import LimitsForm
from periscope.models import Batteries


batteries_blueprint = Blueprint('batteries', __name__, template_folder='templates/batteries')


@batteries_blueprint.route('/batteries', methods=['GET', 'POST'])
def batteries():
    birds_data = {}
    fins_data = {}
    birds_wb = {}
    batt = []
    batt_all = []
    form = LimitsForm()

    if form.validate_on_submit():

        # Dashboard
        birds_wb['wb_birds'] = Batteries.query.with_entities(Batteries.streamer_number,
                                                             Batteries.unit_number) \
                                        .filter(Batteries.bank_b < form.min_v_bank_b.data) \
                                        .filter_by(date_=form.dt.data) \
                                        .filter_by(active_bank='B') \
                                        .filter_by(unit_name='C').all()

        birds_wb['wb_fins'] = Batteries.query.with_entities(Batteries.streamer_number,
                                                            Batteries.unit_number) \
                                       .filter(Batteries.bank_b < form.min_v_bank_b.data) \
                                       .filter_by(date_=form.dt.data) \
                                       .filter_by(active_bank='B') \
                                       .filter_by(unit_name='F').all()

        birds_data['birds_out'] = Batteries.query \
                                           .filter(Batteries.bank_b < form.min_v_bank_b.data) \
                                           .filter_by(date_=form.dt.data) \
                                           .filter_by(active_bank='B') \
                                           .filter_by(unit_name='C').count()

        birds_data['birds_a'] = Batteries.query.filter_by(date_=form.dt.data) \
                                         .filter_by(active_bank='A') \
                                         .filter_by(unit_name='C').count()

        birds_data['birds_b'] = Batteries.query.filter_by(date_=form.dt.data) \
                                         .filter_by(active_bank='B') \
                                         .filter_by(unit_name='C').count()

        fins_data['fins_out'] = Batteries.query.filter(Batteries.bank_b < form.min_v_bank_b.data) \
                                         .filter_by(date_=form.dt.data) \
                                         .filter_by(active_bank='B') \
                                         .filter_by(unit_name='F').count()

        fins_data['fins_a'] = Batteries.query.filter_by(date_=form.dt.data) \
                                       .filter_by(active_bank='A') \
                                       .filter_by(unit_name='F').count()

        fins_data['fins_b'] = Batteries.query.filter_by(date_=form.dt.data) \
                                       .filter_by(active_bank='B') \
                                       .filter_by(unit_name='F').count()

        # Birds
        batt = Batteries.query.filter(Batteries.bank_b < form.min_v_bank_b.data) \
                              .filter_by(date_=form.dt.data) \
                              .filter_by(active_bank='B') \
                              .filter_by(unit_name='C').all()

        batt_all = Batteries.query.with_entities(Batteries.streamer_number, Batteries.unit_number,
                                                 Batteries.bank_a, Batteries.bank_b, Batteries.active_bank) \
                                  .filter_by(date_=form.dt.data).filter_by(unit_name='C').all()

        temp = []
        result = []

        for u in range(1, 30):
            for s in range(1, 7):
                for r in batt_all:
                    if r[0] == s and r[1] == u:
                        temp.append(r)
            result.append(temp)
            temp = []

        # Fins
        batt_f = Batteries.query.filter(Batteries.bank_b < form.min_v_bank_b.data) \
                                .filter_by(date_=form.dt.data) \
                                .filter_by(active_bank='B') \
                                .filter_by(unit_name='F') \
                                .all()

        batt_f_all = Batteries.query.filter_by(date_=form.dt.data).filter_by(unit_name='F').all()

        res = []
        temp = []
        result_f = []

        for u in batt_f_all:
            res.append([u.streamer_number, u.unit_number, u.bank_a, u.bank_b, u.active_bank])

        for u in range(1, 14):
            for s in range(1, 7):
                for r in res:
                    if r[0] == s and r[1] == u:
                        temp.append(r)
            result_f.append(temp)
            temp = []

        return render_template('batteries.html', form=form, batt=batt, result=result,
                               batt_f=batt_f, result_f=result_f, birds_data=birds_data,
                               fins_data=fins_data, birds_wb=birds_wb)

    return render_template('batteries.html', form=form, batt=batt, birds_data=birds_data,
                           fins_data=fins_data, birds_wb=birds_wb)
