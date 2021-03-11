import pandas as pd
import numpy as np

def get_data_div():
    # Define file path
    path_to_csv = 'data/processed/processed_vaccination_data.csv'
    # Get data
    data = pd.read_csv(path_to_csv)
    data['date'] = pd.to_datetime(data['date'], format='%Y-%m-%d')
    # Group by region
    data_div=data.groupby(['division','date','country'],as_index=False).agg(np.nansum).replace(0,np.NaN)
    ## Data cleaning
    # Compute total doses per hundred
    data_div['total_vaccinations_per_hundred'] = (data_div['total_vaccinations_raw'] / data_div['pop_est']) * 100
    # Compute rolling mean of doses per hundred
    data_div['daily_vaccinations_rolling_per_hundred'] = (data_div['daily_vaccinations_rolling'] / data_div['pop_est']) * 100
    # Compute total distributed per hundred
    data_div['total_distributed_raw_per_hundred'] = (data_div['total_distributed_raw'] / data_div['pop_est']) * 100
    # Compute rolling mean of distributed doses per hundred
    data_div['daily_vaccinations_distributed_rolling_per_hundred'] = (data_div['daily_distributed_rolling'] / data_div['pop_est']) * 100
    # Rename columns
    data_div = data_div.rename(columns={'total_vaccinations_per_hundred': 'Total Vaccinations Per 100',
                                'daily_vaccinations_rolling_per_hundred': 'Daily Vaccinations Per 100',
                                'total_distributed_raw_per_hundred': 'Total Distributed Per 100',
                                'daily_vaccinations_distributed_rolling_per_hundred': 'Daily Distributed Per 100',
                                'total_vaccinations_raw': 'Total Vaccinations',
                                'daily_vaccinations_rolling': 'Daily Vaccinations',
                                'total_distributed_raw': 'Total Distributed',
                                'daily_distributed_rolling': 'Daily Distributed'})
    return data_div