import altair as alt
import pandas as pd
import numpy as np

from src.get_data import *
from src.get_data_div import *


def plot_lower_dash(location_choice, my_dropdown, metric_choice, metric_dropdown):
    # Fetch data
    data = get_data()
    data = data.rename(columns={'total_vaccinations_per_hundred': 'Total Vaccinations Per 100',
                                'daily_vaccinations_rolling_per_hundred': 'Daily Vaccinations Per 100',
                                'total_distributed_raw_per_hundred': 'Total Distributed Per 100',
                                'daily_vaccinations_distributed_rolling_per_hundred': 'Daily Distributed Per 100',
                                'total_vaccinations_raw': 'Total Vaccinations',
                                'daily_vaccinations_rolling': 'Daily Vaccinations',
                                'total_distributed_raw': 'Total Distributed',
                                'daily_distributed_rolling': 'Daily Distributed'})
    data_div = get_data_div()
    if location_choice == 'States and Provinces':
        chart = alt.Chart(data, title='State and Provincial Vaccine Data Over Time').mark_line().encode(
            x='date:T',
            y=metric_dropdown,
            color=alt.Color('location', legend=alt.Legend(title="Location")),strokeDash='country:N').transform_filter(
            alt.FieldOneOfPredicate(field='location', oneOf=my_dropdown)).properties(width=800, height=400)

        return chart.to_html()

    elif location_choice == 'Regions':
        region_chart = alt.Chart(data_div, title='Regional Vaccine Data Over Time').mark_line().encode(
            alt.X('date:T', axis=alt.Axis(title='Date')),
            y=metric_dropdown,
            color=alt.Color('division', legend=alt.Legend(title="Region")),
            strokeDash='country:N', ).transform_filter(
            alt.FieldOneOfPredicate(field='division', oneOf=my_dropdown)).properties(width=800, height=400)

        return region_chart.to_html()
