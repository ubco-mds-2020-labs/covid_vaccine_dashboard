import pandas as pd
import numpy as np
import os
import datetime as datetime
import logging
import sys

# Configure logs
logging.basicConfig(filename='logs/fetch_log.log',encoding='utf-8',level=logging.INFO)
logging.info(str(datetime.datetime.now())+': starting script execution')

# Delete flag file if exists
if os.path.isfile('logs/flag.txt'):
    os.remove('logs/flag.txt')

## Read in local datasets
try:
    us_states=pd.read_csv('data/raw/all_states.csv',index_col=0)
    # Add country name to get national data
    us_states.iloc[-1]='United States'
    ca_pop_est=pd.read_csv('data/raw/ca_pop_est.csv',index_col=0)
    regions=pd.read_csv('data/raw/us_canada_regions.csv')
except:
    logging.error(str(datetime.datetime.now())+': reading local CSVs failed')
    logging.error(str(datetime.datetime.now())+': execution halted')
    sys.exit()

## Pull US vaccine data from GitHub
try:
    us_vac=pd.read_csv('https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/vaccinations/us_state_vaccinations.csv')
except:
    logging.error(str(datetime.datetime.now())+': fetching US vaccine data failed')
    logging.error(str(datetime.datetime.now())+': execution halted')
    sys.exit()

## Pull Canada vaccine data from GitHub
try:
    ca_vac_admin=pd.read_csv('https://github.com/ccodwg/Covid19Canada/raw/master/timeseries_prov/vaccine_administration_timeseries_prov.csv')
    ca_vac_dist=pd.read_csv('https://github.com/ccodwg/Covid19Canada/raw/master/timeseries_prov/vaccine_distribution_timeseries_prov.csv')
except:
    logging.error(str(datetime.datetime.now())+': fetching Canada vaccine data failed')
    logging.error(str(datetime.datetime.now())+': execution halted')
    sys.exit()

try:
    ## Clean US dataset
    # Filter out territories, gov agencies, etc
    us_vac=us_vac[us_vac['location'].isin(us_states['all_states'].values)]
    # Convert to datetime
    us_vac['date']=pd.to_datetime(us_vac['date'],format='%Y-%m-%d')
    # Compute population estimates
    us_vac['pop_est']=(us_vac['total_vaccinations']*100)/us_vac['total_vaccinations_per_hundred']
    # Create df with pop estimates
    us_pop_est=us_vac[['location','pop_est']].groupby('location').agg(np.mean).reset_index()
    # Merge population estimates
    us_vac_pop=pd.merge(left=us_vac.drop(columns='pop_est'),right=us_pop_est,how='inner',on='location')
    # Add country columns
    us_vac_pop['country']='usa'

    ## Clean and merge Canada datasets
    # Rename columns
    ca_vac_admin.rename(columns={'date_vaccine_administered':'date','avaccine':'daily_vaccinations','cumulative_avaccine':'total_vaccinations','province':'location'},inplace=True)
    ca_vac_dist.rename(columns={'date_vaccine_distributed':'date','dvaccine':'daily_distributed','cumulative_dvaccine':'total_distributed','province':'location'},inplace=True)

    # Convert date columns to datetime
    ca_vac_admin['date']=pd.to_datetime(ca_vac_admin['date'],format='%d-%m-%Y')
    ca_vac_dist['date']=pd.to_datetime(ca_vac_dist['date'],format='%d-%m-%Y')
    # Merge datasets
    ca_vac=pd.merge(left=ca_vac_admin,right=ca_vac_dist,how='outer',on=['location','date'])
    # Remove abbreviations
    ca_vac['location']=ca_vac['location'].replace({'BC':'British Columbia','NL':'Newfoundland','NWT':'Northwest Territories','PEI':'Prince Edward Island'})
    # Merge vaccine data with population data
    ca_vac_pop=pd.merge(left=ca_vac,right=ca_pop_est,how='inner',on='location')
    # Add country column
    ca_vac_pop['country']='canada'
    ## Merge US & Canada datasets
    all_vac=pd.concat([us_vac_pop[['date','location','country','total_vaccinations','total_distributed','pop_est']],ca_vac_pop[['date','location','country','total_vaccinations','total_distributed','pop_est']]])
    # Rename columns
    all_vac.rename(columns={'total_vaccinations':'total_vaccinations_raw','total_distributed':'total_distributed_raw'},inplace=True)
    # Start Canada dates at the same time as the USA
    all_vac=all_vac[all_vac['date']>=all_vac[all_vac['country']=='usa']['date'].min()]
    # Add divisions
    all_vac=pd.merge(left=all_vac,right=regions.drop(columns='region'),on='location',how='outer')
    # Remove data after latest date (data can be out of sync between two countries)
    latest_date=np.min([all_vac[all_vac['country']=='canada']['date'].max(),all_vac[all_vac['country']=='usa']['date'].max()])
    if latest_date<np.max([all_vac[all_vac['country']=='canada']['date'].max(),all_vac[all_vac['country']=='usa']['date'].max()]):
        logging.warning(str(datetime.datetime.now())+': countries out of sync')
    all_vac=all_vac[all_vac['date']<=latest_date]
except:
    logging.error(str(datetime.datetime.now())+': data cleaning/merging failed')
    logging.error(str(datetime.datetime.now())+': execution halted')
    sys.exit()

# Check if CSV already exists
if os.path.isfile('data/raw/merged_vaccine_data.csv'):
    # Read in current dataset
    current_vac=pd.read_csv('data/raw/merged_vaccine_data.csv')
    # Change date column to datetime
    current_vac['date']=pd.to_datetime(current_vac['date'],format='%Y-%m-%d')
    # Check if dataframes are equal
    if all_vac.reset_index(drop=True).round(1).equals(current_vac.reset_index(drop=True).round(1)):
        logging.info(str(datetime.datetime.now())+': no new data found')
        logging.info(str(datetime.datetime.now())+': script executed successfully')
        sys.exit()
else:
    logging.warning(str(datetime.datetime.now())+': current CSV not found, new one will be created')

# Write to CSV
try:
    all_vac.to_csv('data/raw/merged_vaccine_data.csv',index=False)
    logging.info(str(datetime.datetime.now())+': new data found, writing to CSV')
    logging.info(str(datetime.datetime.now())+': script executed successfully')
    try:
        # Create/open flag file
        flag=open('logs/flag.txt','x')
        flag.write('')
        flag.close()
    except:
        logging.error(str(datetime.datetime.now())+': flag writing failed')
        logging.error(str(datetime.datetime.now())+': execution halted')
        sys.exit()
except:
    logging.error(str(datetime.datetime.now())+': writing to CSV failed')
    logging.error(str(datetime.datetime.now())+': execution halted')
