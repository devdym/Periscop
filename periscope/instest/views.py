from datetime import datetime
from flask import Blueprint, render_template
from periscope.instest.forms import LimitsForm
from periscope.models import InsTest
from periscope.models import InsTestRes
from sqlalchemy import Date, cast
from iteration_utilities import flatten

instest_blueprint = Blueprint('instest', __name__, template_folder='templates/instest')


@instest_blueprint.route('/instest', methods=['GET', 'POST'])
def instest():
    test = []
    testlim = []
    form = LimitsForm()
    data = []
    out_of_limit = []

    if form.validate_on_submit():
        testlim = InsTestRes.query.with_entities(InsTestRes.sensor_nb, 
                                                 InsTestRes.cap_min, InsTestRes.cap_max,
                                                 InsTestRes.cutoff_min, InsTestRes.cutoff_max,
                                                 InsTestRes.leakage, InsTestRes.noise) \
                                  .filter(cast(InsTestRes.updated, Date) == form.date_.data).all()

        out_of_limit.append(InsTest.query.with_entities(InsTest.ass_sn, InsTest.trace, InsTest.streamer) \
                            .filter(cast(InsTest.updated, Date) == form.date_.data) \
                            .filter((InsTest.cap < testlim[0][1]) | (InsTest.cap > testlim[0][2])) \
                            .filter(InsTest.type == 2).all())
                    
        out_of_limit.append(InsTest.query.with_entities(InsTest.ass_sn, InsTest.trace, InsTest.streamer) \
                            .filter(cast(InsTest.updated, Date) == form.date_.data) \
                            .filter((InsTest.cap < testlim[1][1]) | (InsTest.cap > testlim[1][2])) \
                            .filter(InsTest.type == 3).all())

        out_of_limit.append(InsTest.query.with_entities(InsTest.ass_sn, InsTest.trace, InsTest.streamer) \
                            .filter(cast(InsTest.updated, Date) == form.date_.data) \
                            .filter((InsTest.cap < testlim[2][1]) | (InsTest.cap > testlim[2][2])) \
                            .filter(InsTest.type == 4).all())
                    
        out_of_limit.append(InsTest.query.with_entities(InsTest.ass_sn, InsTest.trace, InsTest.streamer) \
                            .filter(cast(InsTest.updated, Date) == form.date_.data) \
                            .filter((InsTest.cap < testlim[3][1]) | (InsTest.cap > testlim[3][2])) \
                            .filter(InsTest.type == 5).all())

                            # cutoff
        out_of_limit.append(InsTest.query.with_entities(InsTest.ass_sn, InsTest.trace, InsTest.streamer) \
                            .filter(cast(InsTest.updated, Date) == form.date_.data) \
                            .filter((InsTest.cutoff < testlim[0][3]) | (InsTest.cutoff > testlim[0][4])) \
                            .filter(InsTest.type == 2).all())
                    
        out_of_limit.append(InsTest.query.with_entities(InsTest.ass_sn, InsTest.trace, InsTest.streamer) \
                            .filter(cast(InsTest.updated, Date) == form.date_.data) \
                            .filter((InsTest.cutoff < testlim[1][3]) | (InsTest.cutoff > testlim[1][4])) \
                            .filter(InsTest.type == 3).all())

        out_of_limit.append(InsTest.query.with_entities(InsTest.ass_sn, InsTest.trace, InsTest.streamer) \
                            .filter(cast(InsTest.updated, Date) == form.date_.data) \
                            .filter((InsTest.cutoff < testlim[2][3]) | (InsTest.cutoff > testlim[2][4])) \
                            .filter(InsTest.type == 4).all())
                    
        out_of_limit.append(InsTest.query.with_entities(InsTest.ass_sn, InsTest.trace, InsTest.streamer) \
                            .filter(cast(InsTest.updated, Date) == form.date_.data) \
                            .filter((InsTest.cutoff < testlim[3][3]) | (InsTest.cutoff > testlim[3][4])) \
                            .filter(InsTest.type == 5).all())

                            # noise
        out_of_limit.append(InsTest.query.with_entities(InsTest.ass_sn, InsTest.trace, InsTest.streamer) \
                            .filter(cast(InsTest.updated, Date) == form.date_.data) \
                            .filter(InsTest.noise > testlim[0][6]) \
                            .filter(InsTest.type == 2).all())
                    
        out_of_limit.append(InsTest.query.with_entities(InsTest.ass_sn, InsTest.trace, InsTest.streamer) \
                            .filter(cast(InsTest.updated, Date) == form.date_.data) \
                            .filter(InsTest.noise > testlim[1][6]) \
                            .filter(InsTest.type == 3).all())

        out_of_limit.append(InsTest.query.with_entities(InsTest.ass_sn, InsTest.trace, InsTest.streamer) \
                            .filter(cast(InsTest.updated, Date) == form.date_.data) \
                            .filter(InsTest.noise > testlim[2][6]) \
                            .filter(InsTest.type == 4).all())
                    
        out_of_limit.append(InsTest.query.with_entities(InsTest.ass_sn, InsTest.trace, InsTest.streamer) \
                            .filter(cast(InsTest.updated, Date) == form.date_.data) \
                            .filter(InsTest.noise > testlim[3][6]) \
                            .filter(InsTest.type == 5).all())

        # leakge
        out_of_limit.append(InsTest.query.with_entities(InsTest.ass_sn, InsTest.trace, InsTest.streamer)
                            .filter(cast(InsTest.updated, Date) == form.date_.data)
                            .filter(InsTest.leakage < testlim[0][5])
                            .filter(InsTest.type == 2).all())
                    
        out_of_limit.append(InsTest.query.with_entities(InsTest.ass_sn, InsTest.trace, InsTest.streamer)
                            .filter(cast(InsTest.updated, Date) == form.date_.data)
                            .filter(InsTest.leakage < testlim[1][5])
                            .filter(InsTest.type == 3).all())

        out_of_limit.append(InsTest.query.with_entities(InsTest.ass_sn, InsTest.trace, InsTest.streamer)
                            .filter(cast(InsTest.updated, Date) == form.date_.data)
                            .filter(InsTest.leakage < testlim[2][5])
                            .filter(InsTest.type == 4).all())
                    
        out_of_limit.append(InsTest.query.with_entities(InsTest.ass_sn, InsTest.trace, InsTest.streamer)
                            .filter(cast(InsTest.updated, Date) == form.date_.data)
                            .filter(InsTest.leakage < testlim[3][5])
                            .filter(InsTest.type == 5).all())

        out_list = []
        out_trace_str = []
        out_of_limit = list(flatten(out_of_limit))
        for r in out_of_limit:
            out_list.append(r[0])
            out_trace_str.append([r[1], r[2]])

        test = InsTest.query.with_entities(InsTest.streamer, InsTest.trace, InsTest.ass_sn) \
                            .filter(cast(InsTest.updated, Date) == form.date_.data).all()

        all_in_col = []
        streamer = 1
        sn = None
        trace = []
        i = 1
        streamers = []
        data = []
        temp = []

        for i in test:
            if i[0] == streamer and sn != i[2]:
                all_in_col.append([i[0], i[1], i[2]])
                sn = i[2]
            else:
                if i[0] != streamer:
                    all_in_col.append([i[0], i[1], i[2]])
                    sn = i[2]
                    streamer = streamer + 1

        for pos in all_in_col:
            if pos[1] not in trace:
                trace.append(pos[1])
            if pos[0] not in streamers:
                streamers.append(pos[0])
        i = 1    
        for tr in trace:
            temp.append(i)
            temp.append(str(tr) + '>>' + str(tr + 11))
            for info in all_in_col:
                if info[1] == tr:
                    temp.append(info[2])
            data.append(temp)
            temp = []
            i = i + 1
        
        return render_template('instest.html', form=form, test=data, testlim=testlim, cap_out2=out_list, out_of_limit=out_of_limit)

    return render_template('instest.html', form=form, test=data, testlim=testlim)
