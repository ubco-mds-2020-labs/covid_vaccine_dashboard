import altair as alt
import pandas as pd
import geopandas as gpd
import shapely
import numpy as np

def plot_upper_dash():
    # Define file paths
    path_to_csv='data/processed/processed_vaccination_data.csv'
    path_to_geojson='data/processed/us_canada.geojson'

    # Read in datasets
    data=pd.read_csv(path_to_csv)
    data['date']=pd.to_datetime(data['date'],format='%Y-%m-%d')
    us_can_geojson=gpd.read_file(path_to_geojson)

    ## Data cleaning
    # Merge geospatial and vaccine data
    geo_data=us_can_geojson[['name','geometry']].merge(data,left_on='name',right_on='location',how='outer').drop(columns='name')
    # Move Hawaii to the right
    geo_data.loc[geo_data['location']=='Hawaii','geometry']=geo_data.loc[geo_data['location']=='Hawaii','geometry'].apply(lambda x: shapely.affinity.translate(x,xoff=20,yoff=0))
    # Compute total doses per hundred
    geo_data['total_vaccinations_per_hundred']=(geo_data['total_vaccinations_raw']/geo_data['pop_est'])*100
    # Compute rolling mean of doses per hundred
    geo_data['daily_vaccinations_rolling_per_hundred']=(geo_data['daily_vaccinations_rolling']/geo_data['pop_est'])*100
    # Compute national data for Canada
    ca_nat=geo_data[geo_data['country']=='canada'].drop(columns='geometry').groupby(['date','country']).agg(np.sum).reset_index()
    ca_nat['location']='Canada'
    # Recompute pop-adjusted stats
    ca_nat['total_vaccinations_per_hundred']=(ca_nat['total_vaccinations_raw']/ca_nat['pop_est'])*100
    ca_nat['daily_vaccinations_rolling_per_hundred']=(ca_nat['daily_vaccinations_rolling']/ca_nat['pop_est'])*100
    # Concat with dataset
    geo_data=pd.concat([geo_data,ca_nat])

    # Create df with latest data
    latest_geo_data=geo_data[geo_data['date']==geo_data['date'].max()]

    # Compute summary stats
    us_sum=latest_geo_data[latest_geo_data['location']=='United States'][['total_vaccinations_raw','pop_est']]
    us_sum['country']='usa'
    ca_sum=latest_geo_data[latest_geo_data['location']=='Canada'][['total_vaccinations_raw','pop_est']]
    ca_sum['country']='canada'
    summary=pd.concat([us_sum,ca_sum]).reset_index(drop=True)
    summary['total_vaccinations_per_hundred']=summary[['total_vaccinations_raw','pop_est']].apply(lambda x:(x[0]/x[1])*100,axis=1)

    ## Creating plots
    # Create chart elements
    choro_tooltip=[alt.Tooltip('location:N',title='State/Province'),alt.Tooltip('total_vaccinations_per_hundred:Q',title='Total Doses Administered per 100',format='.2f'),alt.Tooltip('total_vaccinations_raw:Q',title='Total Doses Administered',format='.0f'),alt.Tooltip('pop_est:Q',title='Estimated Population',format='.0f')]
    line_tooltip=[alt.Tooltip('location:N',title='Location')]
    click=alt.selection_single(fields=['location'],init={'location':'California'})
    us_select=alt.selection_single(fields=['location'],init={'location':'United States'})
    ca_select=alt.selection_single(fields=['location'],init={'location':'Canada'})

    # Create summary plot
    last_updated=alt.Chart(pd.DataFrame({'text':[str(latest_geo_data['date'].iloc[0]).split(' ')[0]]})).mark_text(size=20).encode(text='text:N').properties(width=400,height=40,title='Map Last Updated:')
    us_total=alt.Chart(summary[summary['country']=='usa']).mark_text(size=20).encode(text='total_vaccinations_raw:Q').properties(width=400,height=40,title='Total Doses Administered in USA:')
    us_hundred=alt.Chart(summary[summary['country']=='usa'].round(2)).mark_text(size=20).encode(text='total_vaccinations_per_hundred:Q').properties(width=400,height=40,title='Doses Administered per 100 in USA:')
    ca_total=alt.Chart(summary[summary['country']=='canada']).mark_text(size=20).encode(text='total_vaccinations_raw:Q').properties(width=400,height=30,title='Total Doses Administered in Canada:')
    ca_hundred=alt.Chart(summary[summary['country']=='canada'].round(2)).mark_text(size=20).encode(text='total_vaccinations_per_hundred:Q').properties(width=400,height=40,title='Doses Administered per 100 in Canada:')
    vaccines_today=latest_geo_data[(latest_geo_data['location']=='United States')|(latest_geo_data['location']=='Canada')][['daily_vaccinations_raw']].sum().iloc[0]
    total_today=alt.Chart(pd.DataFrame({'vaccines_today':[vaccines_today]})).mark_text(size=20).encode(text='vaccines_today:Q').properties(width=400,height=40,title='Doses Administered Today in USA & Canada:')
    summary_plot=alt.hconcat(alt.vconcat(last_updated,total_today),alt.vconcat(us_total,ca_total),alt.vconcat(us_hundred,ca_hundred))

    left_width=355

    # Create text label plot
    text = alt.Chart(latest_geo_data).mark_text(align='center', size=16, fontWeight='bold').encode(text='location:N').transform_filter(click).properties(width=left_width, height=20)

    # Create map
    base=alt.Chart(latest_geo_data).mark_geoshape(stroke='black',strokeWidth=1).encode().properties(width=750,height=700,title='Total COVID-19 Vaccinations Administered per 100 Residents').project(type='albers')
    choro=alt.Chart(latest_geo_data).mark_geoshape(stroke='black',strokeWidth=0.5).encode(alt.Color('total_vaccinations_per_hundred',type='quantitative',scale=alt.Scale(scheme='blues'),legend=alt.Legend(title='Doses per 100')),tooltip=choro_tooltip).add_selection(click)

    # Create line plots
    #total_line=alt.Chart(geo_data).mark_line().encode(x=alt.X('date',type='temporal',title='Date'),y=alt.Y('total_vaccinations_per_hundred',type='quantitative',title='Total Doses per 100 Residents'),color='location',tooltip=line_tooltip).properties(width=left_width,height=265,title='Total Doses Administered per 100 Residents since '+str(geo_data['date'].min()).split(' ')[0]).add_selection(us_select).add_selection(ca_select).add_selection(click).transform_filter((us_select)|(ca_select)|(click))
    #rolling_line=alt.Chart(geo_data).mark_line().encode(x=alt.X('date',type='temporal',title='Date'),y=alt.Y('daily_vaccinations_rolling_per_hundred',type='quantitative',title='Daily Doses per 100 Residents'),color='location',tooltip=line_tooltip).properties(width=left_width,height=265,title='Daily Doses Administered per 100 Residents since '+str(geo_data['date'].min()).split(' ')[0]).add_selection(us_select).add_selection(ca_select).add_selection(click).transform_filter((us_select)|(ca_select)|(click))

    # Arrange plots
    #upper_plot=alt.vconcat(summary_plot,alt.hconcat(alt.vconcat(text,total_line,rolling_line),base+choro))
    upper_plot = alt.vconcat(summary_plot, alt.hconcat(alt.vconcat(text), base + choro))
    return upper_plot.to_html()