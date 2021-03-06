import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import altair as alt
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np

# -------------------------------------------------------------------------------------
# Read in data from github. Refreshed automatically.
# Remember, data must be in the same file as the python script. This will change when we read in data from Github
data = pd.read_csv('processed_vaccination_data.csv')

# Wrangle data
## Compare vaccine rollout between regions (divisions)
data_div = data.groupby(['division','date', 'country']).apply(lambda x:np.sum(x['total_vaccinations_int'])/np.sum(x['pop_est'])).reset_index().rename(columns={})
data_div = data_div.rename(columns={0: 'div_vaccines_per_capita'})
# Filter the data to only include the most recent date, which is the most relevant for a single map of the cumulative vaccination numbers
max_date_df = data[data.groupby('location').date.transform('max') == data['date']]
max_date_df['per_100_raw'] = 100*max_date_df['total_vaccinations_raw']/max_date_df['pop_est']
# -------------------------------------------------------------------------------------
def plot_altair(xcol):
    chart = alt.Chart(data_div).mark_line().encode(
        x=xcol,
        y='div_vaccines_per_capita',
        tooltip=xcol).interactive()
        print(xcol)
    return chart.to_html()
# -------------------------------------------------------------------------------------
# Setup app and layout/frontend
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
app.layout = dbc.Container([
    html.H1('Canada and United States COVID-19 Dashboard', style={'text-align': 'left'}),
  
            dcc.Dropdown(
                id='xcol-widget',
                value='Alabama',  # REQUIRED to show the plot on the first page load
                options=[{'label': i, 'value': i} for i in data.location.unique()],
                placeholder='Select locations...', multi=True),

            dcc.DatePickerRange(
                id='my-date-picker-range',
                start_date_placeholder_text="Start Period",
                end_date_placeholder_text="End Period",
                calendar_orientation='vertical',),

            html.Iframe(
            id='my_line_chart',
            style={'border-width': '0', 'width': '100%', 'height': '400px'},
            srcDoc=plot_altair(xcol='date'))

            ])

        

# -----------------------------------------------------------------------------------
# Set up callbacks/backend
@app.callback(
    Output('my_line_chart', 'srcDoc'),
    [Input('my-date-picker-range', 'start_date'),
     Input('my-date-picker-range', 'end_date')]
)
    #Input('ycol-widget', 'value'))

def update_output(xcol):
    return plot_altair(xcol)
if __name__ == '__main__':
    app.run_server(debug=True)