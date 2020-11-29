from flask import Blueprint, render_template, redirect, url_for
from periscope import db
from periscope.tension.forms import LimitsForm
from sqlalchemy import Date, cast
from periscope.models import TensionAvg
from bokeh.embed import components
from bokeh.plotting import figure
import numpy as np
from datetime import datetime
from bokeh.models import ColumnDataSource
import pandas as pd

tension_blueprint = Blueprint('tension', __name__, template_folder='templates/tension')

@tension_blueprint.route('/tension', methods=['GET', 'POST'])
def tension():
    form = LimitsForm()
    tension = []

    if form.validate_on_submit():

        tension = TensionAvg.query.with_entities(cast(TensionAvg.date_, Date), TensionAvg.streamer, TensionAvg.tension).all()

        date_range = TensionAvg.query.with_entities(cast(TensionAvg.date_, Date), TensionAvg.date_).distinct(cast(TensionAvg.date_, Date)).order_by(TensionAvg.date_).all()

        temp = []
        result = []

        for u in date_range:
            temp.append(u[0])
            for s in range(1, 7):
                for r in tension:
                    if r[1] == s and r[0] == u[0]:
                        temp.append(r[2])
            result.append(temp)
            temp = []

        source = pd.DataFrame(result, columns=['date', 'str1', 'str2', 'str3', 'str4', 'str5', 'str6'])
        source.set_index('date', inplace=True)
        plot = figure(plot_width=1000, plot_height=400, title="Streamer Tension", toolbar_location="below", x_axis_type="datetime", y_range=(0, 3000))
        plot.background_fill_color = "#272727"
        plot.border_fill_color = "#272727"
        plot.xgrid.visible = False
        plot.ygrid.grid_line_color = "gray"
        plot.ygrid.grid_line_alpha = 0.5
        plot.ygrid.grid_line_dash = [6, 4]
        plot.yaxis.major_label_text_color = "#747474"
        plot.xaxis.major_label_text_color = "#747474"
        plot.xaxis.major_tick_line_color = "#747474"
        plot.yaxis.major_tick_line_color = "#747474"
        plot.line(x='date', y='str1', source=source, line_color="violet", legend_label="Str 1")
        plot.line(x='date', y='str2', source=source, line_color="green", legend_label="Str 2")
        plot.line(x='date', y='str3', source=source, line_color="lightblue", legend_label="Str 3")
        plot.line(x='date', y='str4', source=source, line_color="pink", legend_label="Str 4")
        plot.line(x='date', y='str5', source=source, line_color="orange", legend_label="Str 5")
        plot.line(x='date', y='str6', source=source, line_color="white", legend_label="Str 6")
        plot.legend.background_fill_alpha = 0.1
        plot.legend.label_text_color = "#747474"
        plot.legend.location = "bottom_left"

        script, div = components(plot)
        kwargs = {'script': script, 'div': div}
        kwargs['title'] = 'bokeh-with-flask'

        return render_template('tension.html', form=form, result=result, **kwargs)
    return render_template('tension.html', form=form)
