import pandas as pd
import numpy as np
import json
import os.path

data_file = "COVID_MX_2020.xlsx"
catalog_file = "Catalogos.xlsx"
desc_file = "descriptor.json"

catalogs = {}
mappings = {}
covid_df = None

# LOAD FILES #
##############
def load_files():
    global covid_df
    global mappings

    # READ DESCRIPTOR JSON
    j_file = open(desc_file, "r")
    desc = json.loads(j_file.read())
    mappings = desc["fields"]
    load_catalogs(desc)
    j_file.close()

    if not os.path.exists("export_dataframe.xlsx"):
        # READ MAIN DATA FILE
        print("Loading data source...")
        xl = pd.ExcelFile(data_file)
        covid_df = xl.parse('Hoja1')
        print("The data set contains " + str(covid_df.shape[0]) + " rows by " + str(covid_df.shape[1]) + " columns.")
        print("Done.")

        # CLEAN DATA
        print("Cleaning data...")
        merge_clean_data()
        print("Done.")

        # FILTER COLUMNS
        covid_df_reduced = covid_df[['ENTIDAD_RES','FECHA_INGRESO','FECHA_DEF']]
        covid_df_reduced = covid_df_reduced.loc[covid_df_reduced['CLASIFICACION_FINAL'].str.contains("Confirmado")]

        # SAVE CLEAN AND FILTERED DATA
        covid_df_reduced.to_json(r'super_reduced.json', orient='records')
    else:
        xl = pd.ExcelFile('export_dataframe.xlsx')
        covid_df = xl.parse('Sheet1')

# LOAD CATALOGUES #
###################
def load_catalogs(desc):
    print("Loading catalogs...")
    cat_xl = pd.ExcelFile(catalog_file)

    for i in desc["catalogs"]:
        catalogs[i] = cat_xl.parse(i)
        # CLEAN EMPTY CELLS
        catalogs[i].dropna(inplace=True)
        # CAST NUMERIC VALUES TO INTEGERS
        dtypes = catalogs[i].dtypes.to_dict()
        if 'float64' in dtypes.values():
            for col_nam, typ in dtypes.items():
                if typ == 'float64':
                    catalogs[i][col_nam] = catalogs[i][col_nam].astype(int)

    cat_mun = catalogs["MUNICIPIOS"]
    cat_mun["CODIGO"] = cat_mun["CLAVE_ENTIDAD"].astype(str) + "-" + cat_mun["CLAVE_MUNICIPIO"].astype(str)
    print("Done.")

# MERGE DATA #
##############
def merge_clean_data():
    for fields in mappings:
        field = fields["name"]

        if fields["format"] == "ID":
            covid_df.set_index(field)

        elif fields["format"] == "DATE":
            # CLEAN EMPTY CELLS
            covid_df[field] = pd.to_datetime(covid_df[field], errors='coerce').fillna('')
            # SEPARATE DATE TYPES
            covid_df[field + "_YR"] = covid_df[field].apply(lambda x: x.year if x != '' else x)
            covid_df[field + "_MT"] = covid_df[field].apply(lambda x: x.month if x != '' else x)
            covid_df[field + "_DY"] = covid_df[field].apply(lambda x: x.day if x != '' else x)
            covid_df[field + "_WK"] = covid_df[field].apply(lambda x: x.week if x != '' else x)

        elif fields["format"] == "MUNICIPIOS":
            catalog = catalogs[fields["format"]]
            relation = fields["relation"]
            covid_df[field] = covid_df[relation].astype(str) + "-" + covid_df[field].astype(str)
            covid_df[field].replace(catalog["CODIGO"].values, catalog["MUNICIPIO"].values, inplace=True)

        elif fields["format"] == "ENTIDADES":
            catalog = catalogs[fields["format"]]
            covid_df[field].replace(catalog["CLAVE_ENTIDAD"].values, catalog["ABREVIATURA"].values, inplace=True)

        elif field == "PAIS_NACIONALIDAD":
            wrong_syntax = ["MÃ©xico", "EspaÃ±a", "Estados Unidos de AmÃ©rica", "HaitÃ­"]
            proper_syntax = ["Mexico", "Spain", "USA", "Haiti"]
            covid_df[field].replace(wrong_syntax, proper_syntax, inplace=True)

        elif fields["format"] in catalogs.keys():
            catalog = catalogs[fields["format"]]
            covid_df[field].replace(catalog["CLAVE"].values, catalog["DESCRIPCIÓN"].values, inplace=True)

load_files()
