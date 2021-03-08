import altair as alt
import pandas as pd
import numpy as np
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# Read in data from github. Refreshed automatically.
data = pd.read_csv('/Users/mitchelldecock/Desktop/Master_of_Data_Science/MD_551/Projects/covid_vaccine_dashboard/data/processed/processed_vaccination_data.csv')

## Compare vaccine rollout between regions (divisions)
data_div = data.groupby(['division','date', 'country']).apply(lambda x:np.sum(x['total_vaccinations_int'])/np.sum(x['pop_est'])).reset_index().rename(columns={})

data_div = data_div.rename(columns={0: 'div_vaccines_per_capita'})

alt.Chart(data_div, title="United States and Canada Regional Vaccination per capita").mark_line().encode(
    alt.X('date:T',
         axis=alt.Axis(title='Date')),
    alt.Y('div_vaccines_per_capita:Q',
          axis=alt.Axis(title='Vaccination rate per capita')),
    color=alt.Color('division', legend=alt.Legend(title="Region")),
    strokeDash='country:N',
).properties(height=500, width=800).configure_legend(
titleFontSize=18,
labelFontSize=15
).configure_axis(
    labelFontSize=10,
    titleFontSize=20
).configure_title(fontSize=24


app = dash.Dash(__name__, external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])

app.layout = html.Div([
    'This is my slider',
    dcc.Slider(min=0, max=5, value=2, marks={0: '0', 5: '5'}),

    html.H1('Hello Dash'),

    html.Div([
        html.P('Dash converts Python classes into HTML'),
        html.P("This conversion happens behind the scenes by Dash's JavaScript front-end")]),
    
    'This is my dropdown',
    dcc.Dropdown(
        id='ycol-widget',
        value='total_vaccinations_raw',
        options=[
            {'label': 'Alaska', 'value': 'Alaska'}, 
            {'label': 'Alabama', 'value': 'Alabama'},
            {'label': 'Arkansas', 'value': 'Arkansas'},
            {'label': 'Arizona', 'value': 'Arizona'},
            {'label': 'California', 'value': 'California'},
            {'label': 'Colorado', 'value': 'Colorado'},
            {'label': 'Connecticut', 'value': 'Connecticut'},
            {'label': 'District of Columbia', 'value': 'District of Columbia'},
            {'label': 'Delaware', 'value': 'Delaware'},
            {'label': 'Florida', 'value': 'Florida'},
            {'label': 'Georgia', 'value': 'Georgia'},
            {'label': 'Hawaii', 'value': 'Hawaii'},
            {'label': 'Iowa', 'value': 'Iowa'},
            {'label': 'Idaho', 'value': 'Idaho'},
            {'label': 'Illinois', 'value': 'Illinois'},
            {'label': 'Indiana', 'value': 'Indiana'},
            {'label': 'Kansas', 'value': 'Kansas'},
            {'label': 'Kentucky', 'value': 'Kentucky'},
            {'label': 'Louisiana', 'value': 'Lousiana'},
            {'label': 'Massachusetts', 'value': 'Massachusetts'},
            {'label': 'Maryland', 'value': 'Maryland'},
            {'label': 'Maine', 'value': 'Maine'},
            {'label': 'Michigan', 'value': 'Michigan'},
            {'label': 'Minnesota', 'value': 'Minnesota'},
            {'label': 'Missouri', 'value': 'Missouri'},
            {'label': 'Mississippi', 'value': 'Mississippi'},
            {'label': 'Montana', 'value': 'Montana'},
            {'label': 'North Carolina', 'value': 'North Carolina'},
            {'label': 'North Dakota', 'value': 'North Dakota'},
            {'label': 'Nebraska', 'value': 'Nebraska'},
            {'label': 'New Hampshire', 'value': 'New Hampshire'},
            {'label': 'New Jersey', 'value': 'New Jersey'},
            {'label': 'New Mexico', 'value': 'New Mexico'},
            {'label': 'Nevada', 'value': 'Nevada'},
            {'label': 'New York State', 'value': 'New York State'},
            {'label': 'Ohio', 'value': 'Ohio'},
            {'label': 'Oklahoma', 'value': 'Oklahoma'},
            {'label': 'Oregon', 'value': 'Oregon'},
            {'label': 'Pennsylvania', 'value': 'Pennsylvania'},
            {'label': 'Rhode Island', 'value': 'Rhode Island'},
            {'label': 'South Carolina', 'value': 'South Carolina'},
            {'label': 'South Dakota', 'value': 'South Dakota'},
            {'label': 'Tennessee', 'value': 'Tennessee'},
            {'label': 'Texas', 'value': 'Texas'},
            {'label': 'Utah', 'value': 'Utah'},
            {'label': 'Virginia', 'value': 'Virginia'},
            {'label': 'Vermont', 'value': 'Vermont'},
            {'label': 'Washington', 'value': 'Washington'},
            {'label': 'Wisconsin', 'value': 'Wisconsin'},
            {'label': 'West Virginia', 'value': 'West Virginia'},
            {'label': 'Wyoming', 'value': 'Wyoming'},
            {'label': 'British Columbia', 'value': 'British Columbia'},
            {'label': 'Alberta', 'value': 'Alberta'},
            {'label': 'Saskatchewan', 'value': 'Saskatchewan'},
            {'label': 'Ontario', 'value': 'Ontario'},
            {'label': 'Nunavut', 'value': 'Nunavut'},
            {'label': 'Yukon', 'value': 'Yukon'},
            {'label': 'Prince Edward Island', 'value': 'Prince Edward Island'},
            {'label': 'Northwest Territories', 'value': 'Northwest Territories'},
            {'label': 'Newfoundland', 'value': 'Newfoundland'},
            {'label': 'New Brunswick', 'value': 'New Brunswick'},
            {'label': 'Nova Scotia', 'value': 'Nova Scotia'},
            {'label': 'Quebec', 'value': 'Quebec'},
            {'label': 'Manitoba', 'value': 'Manitoba'}],
            placeholder='Select locations...', multi=True)])

            # Set up callbacks/backend
@app.callback(
    Output('scatter', 'srcDoc'),
    Input('ycol-widget', 'value'))

def update_output():
    return plot_altair()

app.run_server()

if __name__ == '__main__':
    app.run_server(debug=True)
    

