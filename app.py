from flask import render_template
from sqlalchemy import Date, cast, desc

from periscope import app
from periscope.models import InsTest, InsTestRes, TensionAvg


@app.route('/')  # 127.0.0.1:5000
def index():
    # streamer tension card
    tension_last_date = TensionAvg.query.with_entities(TensionAvg.date_) \
                                  .order_by(desc(TensionAvg.date_)).first()
    tension = TensionAvg.query.with_entities(TensionAvg.tension) \
                        .filter(TensionAvg.date_ == tension_last_date) \
                        .order_by(TensionAvg.streamer).all()

    # ins test card
    out_of_limit = [0, 0, 0, 0, 0, 0]
    upd_date = InsTest.query.with_entities(cast(InsTest.updated, Date)) \
                      .order_by(desc(InsTest.updated)).first()

    testlim = InsTestRes.query.with_entities(InsTestRes.sensor_nb,
                                             InsTestRes.cap_min, InsTestRes.cap_max,
                                             InsTestRes.cutoff_min, InsTestRes.cutoff_max,
                                             InsTestRes.leakage, InsTestRes.noise) \
                        .filter(cast(InsTestRes.updated, Date) == upd_date).all()

    for s in range(1, 7):
        for sen in range(2, 6):
            out_of_limit[s - 1] = out_of_limit[s - 1] + (InsTest.query.with_entities(InsTest.ass_sn, InsTest.trace, InsTest.streamer)
                                                                .filter(cast(InsTest.updated, Date) == upd_date)
                                                                .filter((InsTest.cap < testlim[0][1]) | (InsTest.cap > testlim[0][2]))
                                                                .filter(InsTest.type == sen)
                                                                .filter(InsTest.streamer == s).count())

            out_of_limit[s - 1] = out_of_limit[s - 1] + (InsTest.query.with_entities(InsTest.ass_sn, InsTest.trace, InsTest.streamer)
                                                                .filter(cast(InsTest.updated, Date) == upd_date)
                                                                .filter((InsTest.cutoff < testlim[0][3]) | (InsTest.cutoff > testlim[0][4]))
                                                                .filter(InsTest.type == sen)
                                                                .filter(InsTest.streamer == s).count())

            out_of_limit[s - 1] = out_of_limit[s - 1] + (InsTest.query.with_entities(InsTest.ass_sn, InsTest.trace, InsTest.streamer)
                                                                .filter(cast(InsTest.updated, Date) == upd_date)
                                                                .filter(InsTest.noise > testlim[0][6])
                                                                .filter(InsTest.type == sen)
                                                                .filter(InsTest.streamer == s).count())

            out_of_limit[s - 1] = out_of_limit[s - 1] + (InsTest.query.with_entities(InsTest.ass_sn, InsTest.trace, InsTest.streamer)
                                                                .filter(cast(InsTest.updated, Date) == upd_date)
                                                                .filter(InsTest.leakage < testlim[0][5])
                                                                .filter(InsTest.type == sen)
                                                                .filter(InsTest.streamer == s).count())

    all_err = sum(out_of_limit)

    return render_template('home.html', tension_last_date=tension_last_date[0], tension=tension, upd_date=upd_date[0], testlim=testlim, out_of_limit=out_of_limit, all_err=all_err)


if __name__ == '__main__':
    app.run(debug=True)
