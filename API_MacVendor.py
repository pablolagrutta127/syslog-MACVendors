# -*- coding: utf-8 -*-
"""
Created on Sun Feb 21 17:48:11 2021

@author: G502583
"""
import pip

def import_or_install(package):
    try:
        __import__(package)
        print(package, "already installed")
    except ImportError:
        pip.main(['install', package])  
        
mandatory_packages= ['regex','requests','pandas','os']
for package in mandatory_packages:
    import_or_install(package)
    
import regex as re
import requests
import pandas as pd
from pandas import json_normalize
import os



imported_file = "C:/Users/g502583/OneDrive - Sagemcom Broadband SAS/Documents/Telecentro/TLC_3890/6 - Tabanelli wifi issues/Tabanelli_3890_wifi issues/181.46.183.188.log.2"
# parse it as args[]
with open (imported_file, "r") as myfile:
    data=myfile.read()
target_string= re.findall('(\w+[:]+\w+[:]+\w+[:]+\w+[:]+\w+[:]+\w+)',data)
target_string = list(dict.fromkeys(target_string))


df_data_std = pd.DataFrame()
for item in target_string:
    req_url = "https://macvendors.co/api/"+str(item)
    r = requests.get(req_url)#, auth=BearerAuth(api_token))  ## en r guardo la repuesta de la URL, es decir, del servidor

    try:
        dictr = r.json() 
        dictr_norm = json_normalize(r.json())
        dictr_norm['mac'] = item
        dictr_norm['org_name'] = dictr_norm['result.company']
        frames = dictr_norm[['mac','org_name']]
        df_data_std = df_data_std.append([frames], sort=False)
    except:

        dictr_norm['mac'] = item
        dictr_norm['org_name'] = "Not found"
        frames = dictr_norm[['mac','org_name']]
        df_data_std = df_data_std.append([frames], sort=False)
        
path_to_export  = os.path.dirname(os.path.dirname(imported_file))
df_data_std.to_excel(str(path_to_export) + "/STA-List.xlsx")

