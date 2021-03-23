import altair as alt
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from vega_datasets import data


cars = data.cars()

def plot_altair(xcol):
    chart = alt.Chart(cars).mark_point().encode(
        x=xcol,
        y='Displacement',
        tooltip='Horsepower').interactive()
    return chart.to_html()

app = dash.Dash(__name__, external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])

app.layout = html.Div([
        dcc.Dropdown(
            id='xcol', value='Horsepower',
            options=[{'label': i, 'value': i} for i in cars.columns]),
        html.Iframe(
            id='scatter',
            style={'border-width': '0', 'width': '100%', 'height': '400px'},
            srcDoc=plot_altair(xcol='Horsepower'))])

@app.callback(
    Output('scatter', 'srcDoc'),
    Input('xcol', 'value'))
def update_output(xcol):
    return plot_altair(xcol)

if __name__ == '__main__':
    app.run_server(debug=True) 