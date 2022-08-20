# -*- coding: utf-8 -*-
"""
Created on Wed Oct 13 14:18:40 2021

@author: manjy
"""

import pandas as pd
import numpy as np
import csv
c19_file = "dataset/DDW-C19-0000.xlsx"
c08_file = "dataset/DDW-0000C-08.xlsx"


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


def clean_c19df(c19df):
    # ---------------------------------------
    # Renaming the columns
    columns = ["state_code", "district_code", "area_name",
               "type", "education_level", "persons2", "male2", "female2",
               "persons3", "male3", "female3"]
    c19df.columns = columns
    # ---------------------------------------
    # Filtering to get only Total data,
    # And dropping useless columns
    c19df = c19df.drop(["district_code"], axis=1)
    c19df = c19df[c19df.type == "Total"]
    c19df = c19df[c19df.education_level != "Total"]
    c19df = c19df[c19df.education_level != "Literate"]
    
    c19df = c19df.drop(["type"], axis=1)
    c19df = c19df.drop(["male2", "female2", "male3",
                       "female3", "persons2"], axis=1)
    
    # ---------------------------------------
    # Renaming the education level entries
    c19df.loc[c19df.education_level=="Illiterate", "education_level"] = "illiterate"
    c19df.loc[c19df.education_level=="Literate but below primary", "education_level"] = "below_primary"
    c19df.loc[c19df.education_level=="Primary but below middle", "education_level"] = "primary"
    c19df.loc[c19df.education_level=="Middle but below matric/secondary", "education_level"] = "middle"
    c19df.loc[c19df.education_level=="Matric/Secondary but below graduate", "education_level"] = "matric"
    c19df.loc[c19df.education_level=="Graduate and above", "education_level"] = "graduate_and_above"
    # ---------------------------------------
    # converting to int
    c19df.persons3 = c19df.persons3.astype(int)
    #c19df.state_code = c19df.state_code.astype(int)

    return c19df

def clean_c08df(c08df):
    # ---------------------------------------
    # Dropping useless columns and renaming columns
    drop_cols_index = [0,2,6,7,8,10,11,13,14,16,17,19,20,22,23,25,26,28,29,31,32,34,35,37,38,40,41,43,44]
    c08df = c08df.drop(c08df.columns[drop_cols_index], axis=1)
    try:
        c08df.columns=[
            "state_code","area","type","age_group",
            "illiterate","literate","literate_without_education_level",
            "below_primary","primary","middle","matric","HS"
            ,"NTD","TD","graduate_and_above","unclassified"]
    except:
        c08df.columns=[
            "state_code","area","type","age_group",
            "illiterate","literate","literate_without_education_level",
            "below_primary","primary","middle","matric","HS"
            ,"NTD","TD","graduate_and_above","unclassified","null_col"]
    # ---------------------------------------
    # Filtering out useless values
    c08df = c08df[c08df.area.notna()]
    c08df = c08df[c08df.type == "Total"]
    c08df = c08df[c08df.age_group == "All ages"]
    #c08df.state_code = c08df.state_code.astype(int)
    # ---------------------------------------
    # Converting number rows to int
    c08df.illiterate = c08df.illiterate.astype(int)
    c08df.below_primary = c08df.below_primary.astype(int)
    c08df.primary = c08df.primary.astype(int)
    c08df.middle = c08df.middle.astype(int)
    c08df.matric = c08df.matric.astype(int)
    c08df.HS = c08df.HS.astype(int)
    c08df.NTD = c08df.NTD.astype(int)
    c08df.TD = c08df.TD.astype(int)
    c08df.graduate_and_above = c08df.graduate_and_above.astype(int)
    
    # ---------------------------------------
    # Merging matric with HS, NTD, TD
    c08df["matric"] = c08df["matric"] + c08df["HS"] + c08df.NTD + c08df.TD
    return c08df


def get_literacy_ratio(c08df, c19df):
    
    state_codes = c08df.state_code.tolist()
    output = []
    for state_code in state_codes:
        # Iterating over all states
        max_percent = 0
        max_grp = None
        row_c08df = c08df[c08df.state_code == state_code]
        extract_c19df = c19df[c19df.state_code == state_code]
        
        for i in range(len(extract_c19df)):
            # For each state, check each literacy and find max
            row_c19df = extract_c19df.iloc[i]
            literacy_grp = row_c19df.education_level
            row_c19df_literacy_grp_count = row_c19df.persons3
            
            total_literacy_grp_count = row_c08df[literacy_grp].values[0]
            
            percentage = row_c19df_literacy_grp_count / total_literacy_grp_count
            
            # Update Max
            if percentage > max_percent:
                max_percent = percentage
                max_grp = literacy_grp
            
        output.append([state_code, max_grp, max_percent*100])
    return output                
        
            
            

# ---------------------------------------
# Load the Required DF
c19df = get_dataframe_from_excel(filename=c19_file)
c08df = get_dataframe_from_excel(filename=c08_file)
# ---------------------------------------
# Clean the DF

c19df = clean_c19df(c19df)
c08df = clean_c08df(c08df)

output = get_literacy_ratio(c08df, c19df)

literacy_lookup = {
    "illiterate":"Illiterate",
    "below_primary":"Literate but below primary",
    "primary":"Primary but below middle",
    "middle":"Middle but below matric/secondary",
    "matric":"Matric/Secondary but below graduate",
    "graduate_and_above":"Graduate and above",
    }

# Updating literacy grp with proper names
for line in output:
    line[1] = literacy_lookup[line[1]]

header_row = ["state/ut", "literacy-group", "percentage"]
write_to_csv(output, "output/literacy-india.csv", header_row)