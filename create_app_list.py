#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 15 15:25:33 2020

@author: Lorenzo-Mac

Read and merge the various csv files
"""
###import statement##
import pickle
import pandas as pd
import csv
import os

# Directories
mac_dir = "/Users/Lorenzo-Mac/Dropbox/App market - the value of privacy/Scraper/play_store_privacy_crawler/Dataset"
deca_dir = r"C:\Users\Arca\Dropbox\App market - the value of privacy\Scraper\play_store_privacy_crawler\Dataset"
win_dir = r"C:\Users\LORENZO\Dropbox\App market - the value of privacy\Scraper\play_store_privacy_crawler\Dataset"

out_dir = mac_dir

# Name of txt file for storing list of csv file names
csv_filename = "excel_names"
app_id_list = "app_list"

os.chdir(out_dir)

with open(csv_filename + ".txt", "rb") as fp:
    csv_names = pickle.load(fp)
 
#%%
#csv_names = [x +'.csv' for x in csv_names]
dataframes = []

for i in csv_names:
    data = pd.read_csv(i, names = ['url'], usecols = [0])
    dataframes.append(data)
    
data = pd.concat(dataframes, sort = False)
app_id = data['url'].tolist()

app_id = list(dict.fromkeys(app_id))

try:
    
    # Open old list
    with open(app_id_list + ".txt", "rb") as fp:
        app_list = pickle.load(fp)
    
    print('Old list opened, it contains', len(app_list), 'apps \n')
    
    app_id += app_list
    app_id = list(dict.fromkeys(app_id))
    
except:
    
    print('No previously created list found \n')
   
    
# Save new list
with open(app_id_list + ".txt", "wb") as fp:
    pickle.dump(app_id, fp)
    
print('New list saved, it contains', len(app_id), 'apps \n')