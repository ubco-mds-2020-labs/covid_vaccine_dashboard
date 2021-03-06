import pandas as pd
import numpy as np
import os
import datetime as datetime
import logging
import sys

# Configure logs
logging.basicConfig(filename='logs/process_log.log',encoding='utf-8',level=logging.INFO)
logging.info(str(datetime.datetime.now())+': starting script execution')

# Check if new data to processe
if not os.path.isfile('logs/flag.txt'):
    logging.info(str(datetime.datetime.now())+': no new data to process')
    logging.info(str(datetime.datetime.now())+': script executed successfully')
    sys.exit()
else:
    logging.info(str(datetime.datetime.now())+': new data found, processing')

# Read in fetched dataset
try:
    data=pd.read_csv('data/raw/merged_vaccine_data.csv')
    original_len=len(data)
except:
    logging.error(str(datetime.datetime.now())+': reading merged_vaccine_data failed')
    logging.error(str(datetime.datetime.now())+': execution halted')
    sys.exit()

# Perform computations
try:
    # Change date column to datetime
    data['date']=pd.to_datetime(data['date'],format='%Y-%m-%d')
    # Compute daily vaccinations
    daily=data.groupby('location').apply(lambda x:x.set_index('date')[['total_vaccinations_raw','total_distributed_raw']].diff().clip(lower=0)).reset_index().rename(columns={'total_vaccinations_raw':'daily_vaccinations_raw','total_distributed_raw':'daily_distributed_raw'})
    # Compute 7-day rolling mean of daily vaccinations
    rolling=daily.groupby('location').apply(lambda x:x.set_index('date')[['daily_vaccinations_raw','daily_distributed_raw']].rolling(window=7,min_periods=1).mean().clip(lower=0)).rename(columns={'daily_vaccinations_raw':'daily_vaccinations_rolling','daily_distributed_raw':'daily_distributed_rolling'})
    # Merge with original data
    data=data.merge(daily.merge(rolling,on=['location','date']),on=['location','date'])
    if len(data)!=original_len:
        logging.warning(str(datetime.datetime.now())+': length of dataframe differs after processing')
except:
    logging.error(str(datetime.datetime.now())+': computations failed')
    logging.error(str(datetime.datetime.now())+': execution halted')
    sys.exit()

# Write to CSV
try:
    data.to_csv('data/processed/processed_vaccination_data.csv',index=False)
    logging.info(str(datetime.datetime.now())+': script executed successfully')
except:
    logging.error(str(datetime.datetime.now())+': writing to CSV failed')
    logging.error(str(datetime.datetime.now())+': execution halted')
