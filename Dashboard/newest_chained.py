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
path_to_csv='https://raw.githubusercontent.com/ubco-mds-2020-labs/covid_vaccine_dashboard/main/data/processed/processed_vaccination_data.csv'

data=pd.read_csv(path_to_csv)

# Convert date column to datetime
data['date']=pd.to_datetime(data['date'],format='%Y-%m-%d')



# Compute total doses per hundred
data['total_vaccinations_per_hundred']=(data['total_vaccinations_raw']/data['pop_est'])*100

# Compute rolling mean of vaccination doses per hundred
data['daily_vaccinations_rolling_per_hundred']=(data['daily_vaccinations_rolling']/data['pop_est'])*100

# Total vaccines distributed per hundred
data['total_distributed_raw_per_hundred']=(data['total_distributed_raw']/data['pop_est'])*100

# Compute rolling mean of vaccine doses distributed per hundred
data['daily_vaccinations_distributed_rolling_per_hundred']=(data['daily_distributed_rolling']/data['pop_est'])*100


## Compare vaccine rollout between regions (divisions)
group_dict = {'total_vaccinations_raw':'sum',
              'daily_vaccinations_rolling':'sum', 
              'total_distributed_raw':'sum', 
              'daily_distributed_rolling':'sum', 
              'total_vaccinations_per_hundred':'sum', 
              'daily_vaccinations_rolling_per_hundred':'sum', 
              'total_distributed_raw_per_hundred':'sum', 
              'daily_vaccinations_distributed_rolling_per_hundred':'sum'}
data_div = data
data_div = data.groupby(['division','date', 'country'], as_index=False).agg(group_dict)
data_div

 
## Compare vaccine rollout between regions (divisions)
#data_div = data.groupby(['division','date', 'country']).apply(lambda x:np.sum(x['total_vaccinations_raw'])/np.sum(x['pop_est'])).reset_index().rename(columns={})
#data_div = data_div.rename(columns={0: 'div_vaccines_per_100'})

# Filter the data to only include the most recent date, which is the most relevant for a single map of the cumulative vaccination numbers
#max_date_df = data[data.groupby('location').date.transform('max') == data['date']]
#max_date_df['per_100_raw'] = 100*max_date_df['total_vaccinations_raw']/max_date_df['pop_est']
# -------------------------------------------------------------------------------------

def plot_altair(location_choice, my_dropdown, metric_choice, metric_dropdown):
    
    if location_choice == 'States_provinces':

        chart = alt.Chart(data).mark_line().encode(
            x='date:T',
            y= metric_dropdown,
            color=alt.Color('location', legend=alt.Legend(title="Location"))).\
            transform_filter(alt.FieldOneOfPredicate(field='location',oneOf=my_dropdown))
        
        return chart.to_html()

    elif location_choice == 'Regions':
        region_chart = alt.Chart(data_div, title="United States and Canada Regional Vaccination per 100").mark_line().encode(
            alt.X('date:T', axis=alt.Axis(title='Date')),
            y= metric_dropdown,
            color=alt.Color('division', legend=alt.Legend(title="Region")),
            strokeDash='country:N',).\
            transform_filter(alt.FieldOneOfPredicate(field='division',oneOf=my_dropdown))
        
        return region_chart.to_html()
# -------------------------------------------------------------------------------------
# Setup app and layout/frontend
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

all_options = {
    'Regions': data_div.division.unique(),
    'States_provinces': data.location.unique()
}

all_metrics = {
    'per_100': ['total_vaccinations_per_hundred', 'daily_vaccinations_rolling_per_hundred', 'total_distributed_raw_per_hundred', 'daily_vaccinations_distributed_rolling_per_hundred'],
    'raw': ['total_vaccinations_raw', 'daily_vaccinations_rolling', 'total_distributed_raw', 'daily_distributed_rolling']
}

app.layout = dbc.Container([
    html.H1('Canada and United States COVID-19 Dashboard', style={'text-align': 'left'}),
  
            
            dcc.Dropdown(
                id='my_dropdown',
                placeholder='Select locations...', multi=True),

            dcc.RadioItems(
                id='location_choice',
                options=[{'label': k, 'value': k} for k in all_options.keys()],
                value='States_provinces'
            ),  

            html.Label(['Metric',
            dcc.Dropdown(
                id='metric_dropdown',
                placeholder='Select metrics...', multi=False)]
            ),

            dcc.RadioItems(
                id='metric_choice',
                options=[{'label': k, 'value': k} for k in all_metrics.keys()],
                value='per_100'
            ),  

             html.Iframe(
                id='scatter',
                style={'border-width': '0', 'width': '100%', 'height': '400px'})

            ])

        

# -----------------------------------------------------------------------------------
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

# -------------------------
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

# --------------------------


@app.callback(
    dash.dependencies.Output('scatter', 'srcDoc'),
    dash.dependencies.Input('location_choice', 'value'),
    dash.dependencies.Input('my_dropdown', 'value'),
    dash.dependencies.Input('metric_choice', 'value'),
    dash.dependencies.Input('metric_dropdown', 'value')
    )
def set_display_children(location_choice, my_dropdown, metric_choice, metric_dropdown):
    return plot_altair(location_choice, my_dropdown, metric_choice, metric_dropdown)


if __name__ == '__main__':
    app.run_server(debug=True)