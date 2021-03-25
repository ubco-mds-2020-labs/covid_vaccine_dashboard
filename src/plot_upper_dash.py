import altair as alt
import pandas as pd
import geopandas as gpd
import shapely
import numpy as np

from src.get_data import *


def plot_upper_dash():
    # Define file paths
    path_to_geojson = 'data/processed/us_canada.geojson'

    # Read in datasets
    data = get_data()
    us_can_geojson = gpd.read_file(path_to_geojson)

    # Create df with latest data
    latest_data = data[data['date'] == data['date'].max()]

    # Compute summary stats
    us_sum = latest_data[latest_data['location'] == 'United States'][['total_vaccinations_raw', 'pop_est']]
    us_sum['Country'] = 'USA'
    ca_sum = latest_data[latest_data['location'] == 'Canada'][['total_vaccinations_raw', 'pop_est']]
    ca_sum['Country'] = 'Canada'
    summary = pd.concat([us_sum, ca_sum]).reset_index(drop=True)
    summary['total_vaccinations_per_hundred'] = summary[['total_vaccinations_raw', 'pop_est']].apply(
        lambda x: (x[0] / x[1]) * 100, axis=1)
    summary = summary.round(2)

    # Merge geospatial and latest data
    latest_geo_data = us_can_geojson[['name', 'geometry']].merge(latest_data, left_on='name', right_on='location',
                                                                 how='outer').drop(columns='name')
    # Move Hawaii to the right
    latest_geo_data.loc[latest_geo_data['location'] == 'Hawaii', 'geometry'] = latest_geo_data.loc[
        latest_geo_data['location'] == 'Hawaii', 'geometry'].apply(
        lambda x: shapely.affinity.translate(x, xoff=20, yoff=0))

    # Compute individual figures
    vaccines_today = latest_data[(latest_data['location'] == 'United States') | (latest_data['location'] == 'Canada')][
        ['daily_vaccinations_raw']].sum().iloc[0]
    last_updated = str(latest_data['date'].iloc[0]).split(' ')[0]
    data_start = str(data['date'].min()).split(' ')[0]

    # Create summary plot
    summary_text_size = 25
    summary_width = 400
    summary_height = 35

    last_updated_plot = alt.Chart(pd.DataFrame({'text': [last_updated]})).mark_text(size=summary_text_size).encode(
        text='text:N').properties(width=summary_width, height=summary_height, title='Map Last Updated:')
    total_today_plot = alt.Chart(pd.DataFrame({'vaccines_today': [vaccines_today]}).applymap('{:,.0f}'.format)).mark_text(
        size=summary_text_size).encode(text='vaccines_today:Q').properties(width=summary_width, height=summary_height,
                                                                           title='Doses Administered Today in USA & Canada:')

    us_total_plot = alt.Chart(summary[summary['Country'] == 'USA'].applymap('{:,.0f}'.format)).mark_text(size=summary_text_size).encode(
        text='total_vaccinations_raw:Q').properties(width=summary_width, height=summary_height,
                                                    title='Total Doses Administered in USA:')
    us_hundred_plot = alt.Chart(summary[summary['Country'] == 'USA']).mark_text(size=summary_text_size).encode(
        text='total_vaccinations_per_hundred:Q').properties(width=summary_width, height=summary_height,
                                                            title='Doses Administered per 100 in USA:')

    ca_total_plot = alt.Chart(summary[summary['Country'] == 'Canada'].applymap('{:,.0f}'.format)).mark_text(size=summary_text_size).encode(
        text='total_vaccinations_raw:Q').properties(width=summary_width, height=summary_height,
                                                    title='Total Doses Administered in Canada:')
    ca_hundred_plot = alt.Chart(summary[summary['Country'] == 'Canada']).mark_text(size=summary_text_size).encode(
        text='total_vaccinations_per_hundred:Q').properties(width=summary_width, height=summary_height,
                                                            title='Doses Administered per 100 in Canada:')

    summary_plot = alt.hconcat(alt.vconcat(last_updated_plot, total_today_plot),
                               alt.vconcat(us_total_plot, ca_total_plot), alt.vconcat(us_hundred_plot, ca_hundred_plot))

    # Create chart elements
    choro_tooltip = [alt.Tooltip('location:N', title='State/Province'),
                     alt.Tooltip('total_vaccinations_per_hundred:Q', title='Total Doses Administered per 100',
                                 format='.2f'),
                     alt.Tooltip('total_vaccinations_raw:Q', title='Total Doses Administered', format='.0f'),
                     alt.Tooltip('pop_est:Q', title='Estimated Population', format='.0f')]
    line_tooltip = [alt.Tooltip('location:N', title='Location')]
    click_location = alt.selection_single(fields=['Country', 'location'],
                                          init={'Country': 'USA', 'location': 'California'}, empty='none')

    line_height = 265
    left_width = 345

    # Create map
    base = alt.Chart(latest_geo_data).mark_geoshape(stroke='black', strokeWidth=0.5).encode().properties(width=720,
                                                                                                         height=700,
                                                                                                         title='Total COVID-19 Vaccinations Administered per 100 Residents').project(
        type='albers')
    choro = alt.Chart(latest_geo_data).mark_geoshape(stroke='black', strokeWidth=0.5).encode(
        color=alt.condition(click_location, alt.value('darkred'), alt.Color('total_vaccinations_per_hundred', type='quantitative', scale=alt.Scale(scheme='blues'),
                  legend=alt.Legend(title='Doses per 100'))), tooltip=choro_tooltip,).add_selection(click_location)

    # Create line plots
    total_line = alt.Chart(data).mark_line().encode(x=alt.X('date', type='temporal', title='Date'),
                                                    y=alt.Y('total_vaccinations_per_hundred', type='quantitative',
                                                            title='Total Doses per 100 Residents'), color=alt.Color('location', sort = ['Canada']),
                                                    tooltip=line_tooltip).properties(width=left_width,
                                                                                     height=line_height,
                                                                                     title='Total Doses Administered per 100 Residents').add_selection(
        click_location).transform_filter({'or': [click_location, alt.FieldEqualPredicate(field='nat', equal=1)]})
    rolling_line = alt.Chart(data).mark_line().encode(x=alt.X('date', type='temporal', title='Date'),
                                                      y=alt.Y('daily_vaccinations_rolling_per_hundred',
                                                              type='quantitative',
                                                              title='Daily Doses per 100 Residents'), color=alt.Color('location', sort = ['Canada']),
                                                      tooltip=line_tooltip).properties(width=left_width,
                                                                                       height=line_height,
                                                                                       title='Daily Doses Administered per 100 Residents').add_selection(
        click_location).transform_filter({'or': [click_location, alt.FieldEqualPredicate(field='nat', equal=1)]})

    # Create text label plot
    state_label = alt.Chart(latest_data).mark_text(align='center', size=25, fontWeight='bold').encode(
        text='location:N').properties(width=left_width, height=35).transform_filter(click_location)

    # Arrange plots
    upper_plot = alt.vconcat(summary_plot,
                             alt.hconcat(alt.vconcat(state_label, total_line, rolling_line), base + choro)
                            ).configure_axis(
                                labelFontSize=15,
                                titleFontSize=15
                            ).configure_title(
                                fontSize=20
                            ).configure_legend(
                                titleFontSize=18,
                                labelFontSize=15
                            ) 
    return upper_plot.to_html()
