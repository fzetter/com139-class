import pandas as pd
import numpy as np
import json
import os.path

data_file = "COVID_MX_2020_tst.xlsx"
catalog_file = "Catalogos.xlsx"
desc_file = "descriptor.json"
columns = ['ID_REGISTRO','SEXO','EDAD','ENTIDAD_RES','PAIS_NACIONALIDAD','FECHA_INGRESO','FECHA_DEF',
          'INTUBADO','NEUMONIA','DIABETES','EPOC','ASMA','INMUSUPR','HIPERTENSION','OTRA_COM',
          'CARDIOVASCULAR','OBESIDAD','RENAL_CRONICA','TABAQUISMO','OTRO_CASO','CLASIFICACION_FINAL']

final_columns = ['ID_REGISTRO','SEXO','EDAD','ENTIDAD_RES','MES_INGRESO','MES_DEF',
          'INTUBADO','NEUMONIA','DIABETES','EPOC','ASMA','INMUSUPR','HIPERTENSION','OTRA_COM',
          'CARDIOVASCULAR','OBESIDAD','RENAL_CRONICA','TABAQUISMO','OTRO_CASO']

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

    # READ MAIN DATA FILE
    print("Loading data source...")
    xl = pd.ExcelFile(data_file)
    covid_df = xl.parse('Hoja1')
    print("The data set contains " + str(covid_df.shape[0]) + " rows by " + str(covid_df.shape[1]) + " columns.")
    print("Done.")

    covid_df = covid_df.filter(items=columns)

    # CLEAN DATA
    print("Cleaning data...")
    merge_clean_data()
    print("Done.")

    # FILTER COLUMNS
    covid_df_reduced = covid_df.loc[covid_df['PAIS_NACIONALIDAD'].str.contains("MÃ©xico")]
    #covid_df_reduced = covid_df_reduced.loc[covid_df_reduced['CLASIFICACION_FINAL'].str.contains("Confirmado")]
    covid_df_reduced = covid_df_reduced.filter(items=final_columns)

    print("Final: " + str(covid_df_reduced.shape[0]) + " rows.")

    # SAVE CLEAN AND FILTERED DATA
    #covid_df_reduced.to_json(r'super_reduced.json', orient='records')
    covid_df_reduced.to_excel(r'super_reduced_tst.xlsx', index=False, header=True)

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

        if field in columns:
            if fields["format"] == "ID":
                covid_df.set_index(field)

            elif fields["format"] == "DATE":
                covid_df[field] = pd.to_datetime(covid_df[field], errors='coerce').fillna('')
                covid_df["MES_" + field.split("_")[1]] = covid_df[field].apply(lambda x: get_month(x.month) if x != '' else x)

            elif fields["format"] == "ENTIDADES":
                catalog = catalogs[fields["format"]]
                covid_df[field].replace(catalog["CLAVE_ENTIDAD"].values, catalog["ABREVIATURA"].values, inplace=True)

            elif fields["format"] in catalogs.keys():
                catalog = catalogs[fields["format"]]
                covid_df[field].replace(catalog["CLAVE"].values, catalog["DESCRIPCIÓN"].values, inplace=True)

                if (fields["format"] == "SI_NO"):
                    wrong_syntax = ["SI", "NO", "NO APLICA", "SE IGNORA", "NO ESPECIFICADO"]
                    proper_syntax = ["SI", "NO", "NO", "NO", "NO"]
                    covid_df[field].replace(wrong_syntax, proper_syntax, inplace=True)

# OBATAIN MES #
###############
def get_month(month):
    if (month == 1): return "Jan"
    elif (month == 2): return "Feb"
    elif (month == 3): return "Mar"
    elif (month == 4): return "Apr"
    elif (month == 5): return "May"
    elif (month == 6): return "Jun"
    elif (month == 7): return "Jul"
    elif (month == 8): return "Aug"
    elif (month == 9): return "Sep"
    elif (month == 10): return "Oct"
    elif (month == 11): return "Nov"
    elif (month == 12): return "Dec"
    else: return ""

load_files()
