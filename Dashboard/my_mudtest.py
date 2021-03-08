import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import altair as alt
from vega_datasets import data
import dash_bootstrap_components as dbc


# Read in global data
cars = data.cars()

# Setup app and layout/frontend
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
app.layout = dbc.Container([
    html.H1('My mudplank'),
    dbc.Row([
        dbc.Col([
            dcc.Dropdown(
                id='xcol-widget',
                value='Horsepower',  # REQUIRED to show the plot on the first page load
                options=[{'label': col, 'value': col} for col in cars.columns]),
            dcc.Dropdown(
                id='ycol-widget',
                value='Displacement',  # REQUIRED to show the plot on the first page load
                options=[{'label': col, 'value': col} for col in cars.columns])],
            md=4),
        dbc.Col([
            dbc.Row([
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(html.H5('Key value')),
                        color='warning')),
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(html.H5('Key value')),
                        color='info', inverse=True, style={'text-align': 'center'}))]),
            html.Iframe(
                id='scatter',
                style={'border-width': '0', 'width': '100%', 'height': '400px'})])])])
# Set up callbacks/backend
@app.callback(
    Output('scatter', 'srcDoc'),
    Input('xcol-widget', 'value'),
    Input('ycol-widget', 'value'))
def plot_altair(xcol, ycol):
    chart = alt.Chart(cars).mark_point().encode(
        x=xcol,
        y=ycol,
        tooltip='Horsepower').interactive()
    return chart.to_html()

if __name__ == '__main__':
    app.run_server(debug=True)