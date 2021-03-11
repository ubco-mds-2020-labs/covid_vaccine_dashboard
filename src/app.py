import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output

from src.plot_upper_dash import *

app = dash.Dash()
server=app.server
app.layout = html.Div([
    html.Div('USA & Canada COVID-19 Vaccination Rollout Dashboard', style={'color': 'blue',
                                                                           'font-family': 'sans-serif',
                                                                           'font-size': 44,
                                                                           'marginTop': 50
                                                                           }),
    # html.H1('Summary Stats and Clickable Map', style={'font-familt': 'sans-serif',
    #                                                  'marginTop': 20
    #                                                  }),
    html.P(
        'Hover over a state/province for more information on its current vaccination progress, or click to examine its vaccination rollout over time via the plots on the left.',
        style={'font_family': 'sans-serif'}),
    html.Iframe(srcDoc=plot_upper_dash(),
                style={'width': '100%',
                       'height': '1100px',
                       'border-width': '0px'}),
    # html.H1('State, Province, and Regional Comparisons', style={'marginTop':0}),
    # html.P('Please select areas of interest and a date range to see detailed comparisons.'),
    # html.Iframe(srcDoc = chart.to_html(),
    #            style={'width':'100%',
    #                    'height':'1100px',
    #                    'border-width':'0px'})
])

if __name__ == '__main__':
    app.run_server(debug=True)
