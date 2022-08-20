# -*- coding: utf-8 -*-
"""
Created on Tue Oct 12 20:36:58 2021

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
    c18df = c18df.drop(["male2", "female2", "male3",
                       "female3", "persons2"], axis=1)
    # ---------------------------------------
    # Converting to int
    c18df.persons3 = c18df.persons3.astype(int)
    #c18df.state_code = c18df.state_code.astype(int)
    # ---------------------------------------
    # Grouping by here has no significance,
    # But doing so that Age grp is string wise sorted,
    # This is because c14 is also group by

    c18df = c18df.groupby(
        ["state_code", "age_group", "persons3"]).sum().reset_index()

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
    c14df = c14df[["state_code", "area_name", "age_group", "TPersons"]]
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
    c14df.TPersons = c14df.TPersons.astype(int)
    #c14df.state_code = c14df.state_code.astype(int)
    # ---------------------------------------
    # Groupby will perform actual merging
    c14df = c14df.groupby(
        ["state_code", "age_group"]).sum().reset_index()

    return c14df


def get_max_age_group(c18df, c14df):
    c18df["percentage"] = (c18df.persons3 / c14df.TPersons) * 100
    state_codes = c18df.state_code.unique().tolist()

    output = []
    for state_code in state_codes:
        # Iterate each state
        extract_c18df = c18df[c18df.state_code == state_code]
        max_index = extract_c18df.percentage.idxmax()

        max_row = extract_c18df.loc[max_index]

        temp = [max_row.state_code,
                max_row.age_group, max_row.percentage]

        output.append(temp)

    return output


# ---------------------------------------
# Load the Required DF
c18df = get_dataframe_from_excel(filename=csv_file)
c14df = pd.read_excel(c14_file)
# ---------------------------------------
# Clean the DF

c18df = clean_c18df(c18df)
c14df = clean_c14df(c14df)

# Driver function
output = get_max_age_group(c18df, c14df)
# Write output to csv
header_row = ["state/ut", "age-group", "percentage"]
write_to_csv(output, "output/age-india.csv", header_row)
