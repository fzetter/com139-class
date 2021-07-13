import pandas as pd
import numpy as np
import json
import pickle
import os.path

data_file = "super_reduced.xlsx"
covid_df = None
data_final = []

columns = ['NEUMONIA','DIABETES','EPOC','ASMA','INMUSUPR','HIPERTENSION','CARDIOVASCULAR','OBESIDAD','RENAL_CRONICA','TABAQUISMO']
months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']

# LOAD FILES #
##############
def load_files():
    global covid_df

    # READ MAIN DATA FILE
    print("Loading data source...")
    xl = pd.ExcelFile(data_file)
    covid_df = xl.parse('Sheet1')
    print("The data set contains " + str(covid_df.shape[0]) + " rows by " + str(covid_df.shape[1]) + " columns.")
    print("Done.")

    # CONVERT CONDITIONS TO ROWS
    print("Formatting json...")
    for month in months:
        cond = {}
        cond["month"] = month
        cond["conditions"] = []

        for column in columns:
            obj = {}
            obj["name"] = column

            for data in ['MES_INGRESO', 'MES_DEF']:
                byMonth = covid_df.groupby([data, column], as_index=False)["ID_REGISTRO"].count()
                byMonth.rename(columns={"ID_REGISTRO": "COUNT"}, inplace=True)
                thisMonth = byMonth.loc[byMonth[data].str.contains(month)]
                thisMonth = thisMonth.loc[thisMonth[column].str.contains("SI")].sum()
                if data == 'MES_INGRESO': obj["count"] = thisMonth["COUNT"]
                if data == 'MES_DEF': obj["deaths"] = thisMonth["COUNT"]

            cond["conditions"].append(obj)

        data_final.append(cond)

    with open('scatter_data.json', 'w') as f:
        json.dump(data_final, f, default=np_encoder, indent = 6)

def np_encoder(object):
    if isinstance(object, np.generic):
        return object.item()

load_files()
