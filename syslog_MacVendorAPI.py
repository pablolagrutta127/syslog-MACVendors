# -*- coding: utf-8 -*-
"""
Created on Sun Feb 21 17:48:11 2021

@author: Pablo La Grutta
mail: pablo.lg.unlam@gmail.com
"""
import regex as re
import requests
import pandas as pd
from pandas import json_normalize


imported_file = "path/to/text/file"
with open (imported_file, "r") as myfile:
    data=myfile.read()
target_string= re.findall('(\w+[:]+\w+[:]+\w+[:]+\w+[:]+\w+[:]+\w+)',data)
print(target_string)


class BearerAuth(requests.auth.AuthBase):
    def __init__(self, token):
        self.token = token
    def __call__(self, r):
        r.headers["authorization"] = "Bearer " + self.token
        return r

api_token = "MACVendors_API_Token"
[target_string.index(item) for item in target_string]
df_data_std = pd.DataFrame()
for item in target_string:
    req_url = "https://api.macvendors.com/v1/lookup/"+item
    try:
        r = requests.get(req_url, auth=BearerAuth(api_token))  
        dictr = r.json() 
        dictr_norm = json_normalize(r.json())
        dictr_norm['mac'] = item
        dictr_norm['org_name'] = dictr_norm['data.organization_name']
        frames = dictr_norm[['mac','org_name']]
        df_data_std = df_data_std.append([frames], sort=False)
    except:
        dictr_norm['mac'] = item
        dictr_norm['org_name'] = "Not found"
        frames = dictr_norm[['mac','org_name']]
        df_data_std = df_data_std.append([frames], sort=False)


