import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

from src.get_data import *
from src.plot_upper_dash import *
from src.plot_lower_dash import *

app = dash.Dash()
server=app.server

# Fetch data
data = get_data()
data_div = get_data_div()

all_options = {
    'Regions': data_div.division.unique(),
    'States and Provinces': data.location.unique()
}

all_metrics = {
    'Per 100': ['Total Vaccinations Per 100', 'Daily Vaccinations Per 100', 'Total Distributed Per 100',
                'Daily Distributed Per 100'],
    'Total': ['Total Vaccinations', 'Daily Vaccinations', 'Total Distributed', 'Daily Distributed']
}

app.layout = html.Div([
    html.Div('USA & Canada COVID-19 Vaccination Rollout Dashboard', style={'color': 'blue',
                                                                           'font-family': 'sans-serif',
                                                                           'font-size': 44,
                                                                           'marginTop': 50
                                                                           }),
    # html.H1('Summary Stats and Clickable Map', style={'font-family': 'sans-serif',
    #                                                  'marginTop': 20
    #                                                  }),
    html.P(
        'Hover over a state/province for more information on its current vaccination progress, or click to examine its vaccination rollout over time via the plots on the left.',
        style={'font-family': 'sans-serif'}),
    html.Iframe(srcDoc=plot_upper_dash(),
                style={'width': '100%',
                       'height': '1100px',
                       'border-width': '0px'}),
    html.H1('State/Province & Regional Comparisons', style={'font-family': 'sans-serif', 'marginTop': 0}),
    html.P(
        'Select a set of states/regions and a metric to see time series data. Selecting "Per 100" will display the chosen metric per 100 residents.',
        style={'font-family': 'sans-serif'}),
    dbc.Container([
        dbc.Row([
            dbc.Col([
                dcc.Dropdown(
                    id='my_dropdown',
                    placeholder='Select locations...', multi=True,
                    style={'font-family': 'sans-serif'}),

                dcc.RadioItems(
                    id='location_choice',
                    options=[{'label': k, 'value': k} for k in all_options.keys()],
                    style={'font-family': 'sans-serif'},
                    value='States and Provinces'
                ),

                dcc.Dropdown(
                    id='metric_dropdown',
                    placeholder='Select metrics...', multi=False,
                    style={'height': '40px', 'width': '300px', 'display': 'inline-block', 'font-family': 'sans-serif'},
                    value=['California','British Columbia']
                ),

                dcc.RadioItems(
                    id='metric_choice',
                    options=[{'label': k, 'value': k} for k in all_metrics.keys()],
                    value='Per 100',
                    style={'font-family': 'sans-serif'},
                )], md=4),

            dbc.Col(
                html.Iframe(
                    id='scatter',
                    style={'border-width': '0', 'width': '1200px', 'height': '600px', 'font-family': 'sans-serif'}
                )

            )])])
])


# Set up callbacks/backend
@app.callback(
    dash.dependencies.Output('my_dropdown', 'options'),
    dash.dependencies.Input('location_choice', 'value'))
def update_my_output(location_choice):
    return [{'label': i, 'value': i} for i in all_options[location_choice]]


@app.callback(
    Output('my_dropdown', 'value'),
    Input('my_dropdown', 'options'))
def set_states_value(available_options):
    return available_options[0]['value']


@app.callback(
    dash.dependencies.Output('metric_dropdown', 'options'),
    dash.dependencies.Input('metric_choice', 'value'))
def update_output(metric_choice):
    return [{'label': i, 'value': i} for i in all_metrics[metric_choice]]


@app.callback(
    Output('metric_dropdown', 'value'),
    Input('metric_dropdown', 'options'))
def set_metrics_value(available_options):
    return available_options[0]['value']


@app.callback(
    dash.dependencies.Output('scatter', 'srcDoc'),
    dash.dependencies.Input('location_choice', 'value'),
    dash.dependencies.Input('my_dropdown', 'value'),
    dash.dependencies.Input('metric_choice', 'value'),
    dash.dependencies.Input('metric_dropdown', 'value')
)
def set_display_children(location_choice, my_dropdown, metric_choice, metric_dropdown):
    return plot_lower_dash(location_choice, my_dropdown, metric_choice, metric_dropdown)


if __name__ == '__main__':
    app.run_server(debug=True)
