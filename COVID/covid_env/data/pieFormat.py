import pandas as pd
import numpy as np
import json
import pickle
import os.path

data_file = "super_reduced.xlsx"
covid_df = None
data_final = {}

columns = ['NEUMONIA','DIABETES','EPOC','ASMA','INMUSUPR','HIPERTENSION','CARDIOVASCULAR','OBESIDAD','RENAL_CRONICA','TABAQUISMO']

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
    for column in columns:
        byCond = covid_df.groupby([column], as_index=False)["ID_REGISTRO"].count()
        byCond.rename(columns={"ID_REGISTRO": "COUNT"}, inplace=True)
        byCond = byCond.loc[byCond[column].str.contains("SI")].sum()
        data_final[column] = byCond["COUNT"]
    print("Done.")

    with open('pie_data.json', 'w') as f:
        json.dump(data_final, f, default=np_encoder, indent = 6)

def np_encoder(object):
    if isinstance(object, np.generic):
        return object.item()

load_files()
