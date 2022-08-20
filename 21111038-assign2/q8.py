# -*- coding: utf-8 -*-
"""
Created on Thu Nov  4 11:26:52 2021

@author: manjy
"""


import pandas as pd
import numpy as np
import csv
csv_file = "dataset/DDW-C18-0000.xlsx"
c14_file = "dataset/DDW-0000C-14.xls"


def get_dataframe_from_excel(filename):

    df = pd.read_excel(filename, engine="openpyxl")
    return df


def write_to_csv(rows, filename, header_row):
    """Write list to csv

    Args:
        rows (list): Target list to be outputted
        filename (str): Output file name with extension
        header_row (list): Header of the csv
    """
    with open(filename, "w", newline="") as f:
        write = csv.writer(f)
        write.writerow(header_row)
        for row in rows:
            write.writerow(row)

def clean_c18df(c18df):
    # ---------------------------------------
    # Renaming the columns
    columns = ["state_code", "district_code", "area_name",
               "type", "age_group", "persons2", "male2", "female2",
               "persons3", "male3", "female3"]

    c18df.columns = columns
    # ---------------------------------------
    # Filtering to get only Total data,
    # And dropping useless columns

    c18df = c18df.drop(["district_code"], axis=1)
    c18df = c18df[c18df.age_group != "Total"]
    c18df = c18df[c18df.age_group != "Age not stated"]
    c18df = c18df[c18df.type == "Total"]
    c18df = c18df.drop(["type"], axis=1)
    c18df = c18df.drop(["persons2", "persons3"], axis=1)
    # ---------------------------------------
    # Converting to int
    c18df.male2 = c18df.male2.astype(int)
    c18df.male3 = c18df.male3.astype(int)

    
    c18df.female2 = c18df.female2.astype(int)
    c18df.female3 = c18df.female3.astype(int)
    
    # number of people speaking 2 languages contain
    # 3 languages 2. Using this to extract only 
    # Person speaking exactly 2
    c18df.male2 = c18df.male2 - c18df.male3
    c18df.female2 = c18df.female2 - c18df.female3
    
    #c18df.state_code = c18df.state_code.astype(int)
    # ---------------------------------------
    # Grouping by here has no significance,
    # But doing so that Age grp is string wise sorted,
    # This is because c14 is also group by

    c18df = c18df.groupby(
        ["state_code", "area_name", "age_group", "male2", "female2", "male3", "female3"]).sum().reset_index()

    return c18df
    # ---------------------------------------


def clean_c14df(c14df):
    # Renaming the columns
    columns = [
        'table', 'state_code', 'district_code', 'area_name',
        'age_group', 'TPersons', 'TMale', 'TFemale',
        'RPersons', 'RMale', 'RFemale',
        'UPersons', 'UMale', 'UFemale']
    c14df.columns = columns
    # ---------------------------------------
    # Extracting required columns
    c14df = c14df[["state_code", "area_name", "age_group", "TMale", "TFemale"]]
    # ---------------------------------------    
    # Filtering out unnecessary rows
    c14df = c14df[c14df.age_group != "All ages"]
    c14df = c14df[c14df.age_group != "0-4"]
    c14df = c14df[c14df.age_group != "Age not stated"]
    c14df = c14df[c14df.age_group != "Age-group"]
    c14df = c14df[c14df.age_group != "nan"]
    c14df = c14df[c14df.area_name.notna()]
    # ---------------------------------------
    # Merging age groups that have finer division
    c14df.loc[c14df.age_group == "30-34", "age_group"] = "30-49"
    c14df.loc[c14df.age_group == "35-39", "age_group"] = "30-49"
    c14df.loc[c14df.age_group == "40-44", "age_group"] = "30-49"
    c14df.loc[c14df.age_group == "45-49", "age_group"] = "30-49"

    c14df.loc[c14df.age_group == "50-54", "age_group"] = "50-69"
    c14df.loc[c14df.age_group == "55-59", "age_group"] = "50-69"
    c14df.loc[c14df.age_group == "60-64", "age_group"] = "50-69"
    c14df.loc[c14df.age_group == "65-69", "age_group"] = "50-69"

    c14df.loc[c14df.age_group == "70-74", "age_group"] = "70+"
    c14df.loc[c14df.age_group == "75-79", "age_group"] = "70+"
    c14df.loc[c14df.age_group == "80+", "age_group"] = "70+"
    # ---------------------------------------
    # Converting to int
    c14df.TMale = c14df.TMale.astype(int)
    c14df.TFemale = c14df.TFemale.astype(int)
    c14df.state_code = c14df.state_code.astype(int)
    # ---------------------------------------
    # Groupby will perform actual merging
    c14df = c14df.groupby(
        ["state_code", "area_name", "age_group"]).sum().reset_index()

    return c14df


def get_max_age_group(c18df, c14df):
    # Finding the required percentages and values
    c18df["male1"] = c14df.TMale - c18df.male2 - c18df.male3
    c18df["female1"] = c14df.TFemale - c18df.female2 - c18df.female3
    
    c18df["M1percentage"] = (c18df.male1 / c14df.TMale) 
    c18df["F1percentage"] = (c18df.female1 / c14df.TFemale) 
    c18df["M2percentage"] = (c18df.male2 / c14df.TMale) 
    c18df["F2percentage"] = (c18df.female2 / c14df.TFemale) 
    c18df["M3percentage"] = (c18df.male3 / c14df.TMale) 
    c18df["F3percentage"] = (c18df.female3 / c14df.TFemale) 
    
    
    state_codes = c18df.state_code.unique().tolist()

    output3 = []
    output2 = []
    output1 = []
    for state_code in state_codes:
        # Iterating over states
        extract_c18df = c18df[c18df.state_code == state_code]
        
        # Handling one lang speakers
        male1_max_index = extract_c18df.M1percentage.idxmax()
        male1_max_row = extract_c18df.loc[male1_max_index]
        female1_max_index = extract_c18df.F1percentage.idxmax()
        female1_max_row = extract_c18df.loc[female1_max_index]

        temp = [male1_max_row.state_code,
                male1_max_row.age_group, male1_max_row.M1percentage, 
                female1_max_row.age_group, female1_max_row.F1percentage]
        output1.append(temp)
        
        # Handling two lang speakers
        male2_max_index = extract_c18df.M2percentage.idxmax()
        male2_max_row = extract_c18df.loc[male2_max_index]
        female2_max_index = extract_c18df.F2percentage.idxmax()
        female2_max_row = extract_c18df.loc[female2_max_index]

        temp = [male2_max_row.state_code,
                male2_max_row.age_group, male2_max_row.M2percentage, 
                female2_max_row.age_group, female2_max_row.F2percentage]
        output2.append(temp)
        
        # Handling three lang speakers
        male3_max_index = extract_c18df.M3percentage.idxmax()
        male3_max_row = extract_c18df.loc[male3_max_index]
        female3_max_index = extract_c18df.F3percentage.idxmax()
        female3_max_row = extract_c18df.loc[female3_max_index]

        temp = [male3_max_row.state_code,
                male3_max_row.age_group, male3_max_row.M3percentage, 
                female3_max_row.age_group, female3_max_row.F3percentage]
        output3.append(temp)
        
        

    return output1, output2, output3


# ---------------------------------------
# Load the Required DF
c18df = get_dataframe_from_excel(filename=csv_file)
c14df = pd.read_excel(c14_file, engine="xlrd")
# ---------------------------------------
# Clean the DF

c18df = clean_c18df(c18df)
c14df = clean_c14df(c14df)


output1, output2, output3 = get_max_age_group(c18df, c14df)
header_row = ["state/ut", "age-group-males", "ratio-males", 
              "age-group-females", "ratio-females"]



write_to_csv(output3, "output/age-gender-a.csv", header_row)
write_to_csv(output2, "output/age-gender-b.csv", header_row)
write_to_csv(output1, "output/age-gender-c.csv", header_row)
