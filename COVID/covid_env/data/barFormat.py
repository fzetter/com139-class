import pandas as pd
import numpy as np
import json
import pickle
import os.path

data_file = "super_reduced.xlsx"
covid_df = None
data_final = {}

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
    acum_dia = covid_df.groupby(["ENTIDAD_RES"], as_index=False)["ID_REGISTRO"].count()
    acum_dia.rename(columns={"ID_REGISTRO": "COUNT"}, inplace=True)
    acum_dia.to_json(r'bar_data.json', orient='records')

def np_encoder(object):
    if isinstance(object, np.generic):
        return object.item()

load_files()
