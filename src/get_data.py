import pandas as pd
import numpy as np


def get_data():
    # Define file path
    path_to_csv = 'data/processed/processed_vaccination_data.csv'
    data = pd.read_csv(path_to_csv)
    data['date'] = pd.to_datetime(data['date'], format='%Y-%m-%d')
    ## Data cleaning
    ## Compute national data for Canada
    ca_nat = data[data['country'] == 'canada'].groupby(['date', 'country']).agg(np.sum).reset_index()
    ca_nat['location'] = 'Canada'
    # Re-compute population-adjusted stats
    ca_nat.drop(columns=['daily_vaccinations_rolling', 'daily_distributed_rolling', 'daily_vaccinations_raw',
                         'daily_distributed_raw'], inplace=True)
    # Compute daily vaccinations
    daily = ca_nat.groupby('location').apply(
        lambda x: x.set_index('date')[['total_vaccinations_raw', 'total_distributed_raw']].diff().clip(
            lower=0)).reset_index().rename(
        columns={'total_vaccinations_raw': 'daily_vaccinations_raw', 'total_distributed_raw': 'daily_distributed_raw'})
    # Compute 7-day rolling mean of daily vaccinations
    rolling = daily.groupby('location').apply(
        lambda x: x.set_index('date')[['daily_vaccinations_raw', 'daily_distributed_raw']].rolling(window=7,
                                                                                                   min_periods=1).mean().clip(
            lower=0)).rename(columns={'daily_vaccinations_raw': 'daily_vaccinations_rolling',
                                      'daily_distributed_raw': 'daily_distributed_rolling'})
    # Merge back
    ca_nat = ca_nat.merge(daily.merge(rolling, on=['location', 'date']), on=['location', 'date'])
    # Concat with dataset
    data = pd.concat([data, ca_nat])
    ## Compute population-adjusted metrics
    # Compute total doses per hundred
    data['total_vaccinations_per_hundred'] = (data['total_vaccinations_raw'] / data['pop_est']) * 100
    # Compute rolling mean of doses per hundred
    data['daily_vaccinations_rolling_per_hundred'] = (data['daily_vaccinations_rolling'] / data['pop_est']) * 100
    # Compute total distributed per hundred
    data['total_distributed_raw_per_hundred'] = (data['total_distributed_raw'] / data['pop_est']) * 100
    # Compute rolling mean of distributed doses per hundred
    data['daily_vaccinations_distributed_rolling_per_hundred'] = (data['daily_distributed_rolling'] / data[
        'pop_est']) * 100
    # Create nat column
    data['nat'] = 0
    data.loc[(data['location'] == 'Canada') | (data['location'] == 'United States'), 'nat'] = 1
    # Rename country column and values to have correct capitalization
    data.rename(columns={'country':'Country'}, inplace=True)
    data.loc[data['Country'] == 'canada', 'Country'] = 'Canada'
    data.loc[data['Country'] == 'usa', 'Country'] = 'USA'
    return data