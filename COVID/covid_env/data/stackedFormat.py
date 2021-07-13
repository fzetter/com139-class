import pandas as pd
import numpy as np
import json
import csv
import pickle
import os.path

data_file = "super_reduced.xlsx"
covid_df = None
data_final = {}
global_i = 0

columns = ['NEUMONIA','DIABETES','EPOC','ASMA','INMUSUPR','HIPERTENSION','CARDIOVASCULAR','OBESIDAD','RENAL_CRONICA','TABAQUISMO']

# LOAD FILES #
##############
def load_files():
    global covid_df
    global global_i

    # READ MAIN DATA FILE
    print("Loading data source...")
    xl = pd.ExcelFile(data_file)
    covid_df = xl.parse('Sheet1')
    print("The data set contains " + str(covid_df.shape[0]) + " rows by " + str(covid_df.shape[1]) + " columns.")
    print("Done.")

    # CONVERT CONDITIONS TO ROWS
    print("Obtaining states...")
    acum_state = covid_df.groupby(["ENTIDAD_RES"], as_index=False)["ID_REGISTRO"].count()
    acum_state.rename(columns={"ID_REGISTRO": "COUNT"}, inplace=True)
    states = acum_state["ENTIDAD_RES"].tolist()
    print("Done.")

    # JSON FORMAT
    print("Formatting json...")
    for state in states:
        cond = {}
        cond["STATE"] = state
        for column in columns:
            acum_cond = covid_df.groupby(["ENTIDAD_RES", column], as_index=False)["ID_REGISTRO"].count()
            acum_cond.rename(columns={"ID_REGISTRO": "COUNT"}, inplace=True)
            acum_cond = acum_cond.loc[acum_cond["ENTIDAD_RES"].str.contains(state)]
            acum_cond = acum_cond.loc[acum_cond[column].str.contains("SI")].sum()
            cond[column] = acum_cond["COUNT"]

        data_final[global_i] = cond
        global_i = global_i + 1

    # EXPORT JSON
    with open('stacked_data.json', 'w') as f:
        json.dump(data_final, f, default=np_encoder, indent = 6)

    # EXPORT JSON AS CSV
    pdObj = pd.read_json('stacked_data.json', orient = 'index')
    pdObj.to_csv('stacked_data.csv', index=False)

def np_encoder(object):
    if isinstance(object, np.generic):
        return object.item()

load_files()
