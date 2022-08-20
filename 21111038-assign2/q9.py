# -*- coding: utf-8 -*-
"""
Created on Thu Nov  4 12:52:01 2021

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
    c19df = c19df.drop(["persons2", "persons3"], axis=1)
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
    c19df.male2 = c19df.male2.astype(int)
    c19df.female2 = c19df.female2.astype(int)
    c19df.male3 = c19df.male3.astype(int)
    c19df.female3 = c19df.female3.astype(int)

    c19df.male2 = c19df.male2 - c19df.male3
    c19df.female2 = c19df.female2 - c19df.female3
    
    c19df.state_code = c19df.state_code.astype(int)

    return c19df

def clean_c08df(c08df):
    # ---------------------------------------
    # Dropping useless columns and renaming columns
    drop_cols_index = [0,2,6,7,8,9,12,15,18,21,24,27,30,33,36,39,42]
    c08df = c08df.drop(c08df.columns[drop_cols_index], axis=1)
    try:
        c08df.columns=[
            "state_code","area","type","age_group",
            "M_illiterate","F_illiterate","M_literate","F_literate",
            "M_literate_without_education_level", "F_literate_without_education_level",
            "M_below_primary", "F_below_primary",
            "M_primary", "F_primary",
            "M_middle", "F_middle",
            "M_matric", "F_matric",
            "M_HS", "F_HS",
            "M_NTD", "F_NTD",
            "M_TD", "F_TD",
            "M_graduate_and_above", "F_graduate_and_above",
            "M_unclassified", "F_unclassified"]
    except:
        c08df.columns=[
            "state_code","area","type","age_group",
            "M_illiterate","F_illiterate","M_literate","F_literate",
            "M_literate_without_education_level", "F_literate_without_education_level",
            "M_below_primary", "F_below_primary",
            "M_primary", "F_primary",
            "M_middle", "F_middle",
            "M_matric", "F_matric",
            "M_HS", "F_HS",
            "M_NTD", "F_NTD",
            "M_TD", "F_TD",
            "M_graduate_and_above", "F_graduate_and_above",
            "M_unclassified", "F_unclassified", "null_col"]
    
    # ---------------------------------------
    # Filtering out useless values
    c08df = c08df[c08df.area.notna()]
    c08df = c08df[c08df.type == "Total"]
    c08df = c08df[c08df.age_group == "All ages"]
    # ---------------------------------------
    # Converting number rows to int
    c08df.state_code = c08df.state_code.astype(int)
    c08df.M_illiterate = c08df.M_illiterate.astype(int)
    c08df.M_below_primary = c08df.M_below_primary.astype(int)
    c08df.M_primary = c08df.M_primary.astype(int)
    c08df.M_middle = c08df.M_middle.astype(int)
    c08df.M_matric = c08df.M_matric.astype(int)
    c08df.M_HS = c08df.M_HS.astype(int)
    c08df.M_NTD = c08df.M_NTD.astype(int)
    c08df.M_TD = c08df.M_TD.astype(int)
    c08df.M_graduate_and_above = c08df.M_graduate_and_above.astype(int)
    
    c08df.F_illiterate = c08df.F_illiterate.astype(int)
    c08df.F_below_primary = c08df.F_below_primary.astype(int)
    c08df.F_primary = c08df.F_primary.astype(int)
    c08df.F_middle = c08df.F_middle.astype(int)
    c08df.F_matric = c08df.F_matric.astype(int)
    c08df.F_HS = c08df.F_HS.astype(int)
    c08df.F_NTD = c08df.F_NTD.astype(int)
    c08df.F_TD = c08df.F_TD.astype(int)
    c08df.F_graduate_and_above = c08df.F_graduate_and_above.astype(int)
    
    # ---------------------------------------
    # Merging matric with HS, NTD, TD
    c08df["M_matric"] = c08df["M_matric"] + c08df["M_HS"] + c08df.M_NTD + c08df.M_TD
    c08df["F_matric"] = c08df["F_matric"] + c08df["F_HS"] + c08df.F_NTD + c08df.F_TD
    return c08df


def find_max_literacy(c08_index, c19_index, state_code, c08df, c19df):
    
    max_percent = 0
    max_grp = None
    row_c08df = c08df[c08df.state_code == state_code]
    extract_c19df = c19df[c19df.state_code == state_code]
    
    for i in range(len(extract_c19df)):
        # iterating over all states
        row_c19df = extract_c19df.iloc[i]
        literacy_grp = row_c19df.education_level
        
        if c19_index == "male" or c19_index == "female":
            
            lang2_c19df_literacy_grp_count = row_c19df[f"{c19_index}2"]
            lang3_c19df_literacy_grp_count = row_c19df[f"{c19_index}3"]
            
            total_literacy_grp_count = row_c08df[f"{c08_index}{literacy_grp}"].values[0]
            row_c19df_literacy_grp_count = total_literacy_grp_count - lang2_c19df_literacy_grp_count - lang3_c19df_literacy_grp_count
            
        else:
            row_c19df_literacy_grp_count = row_c19df[c19_index]
            
            total_literacy_grp_count = row_c08df[f"{c08_index}{literacy_grp}"].values[0]
        
        percentage = row_c19df_literacy_grp_count / total_literacy_grp_count
        
        if percentage > max_percent:
            max_percent = percentage
            max_grp = literacy_grp
    return max_grp, max_percent




def get_literacy_ratio(c08df, c19df):
    
    state_codes = c08df.state_code.tolist()
    output3 = []
    output2 = []
    output1 = []
    

    for state_code in state_codes:
        
        if len(str(state_code))==1:
            str_state_code = f"0{state_code}"
        else:
            str_state_code = str(state_code)
        
        # Handling three language speakers
        male3_grp, male3_percent = find_max_literacy("M_", "male3", state_code, c08df, c19df)
        female3_grp, female3_percent = find_max_literacy("F_", "female3", state_code, c08df, c19df)
        output3.append([str_state_code, male3_grp, male3_percent, female3_grp, female3_percent])

        # Handling two language speakers
        male2_grp, male2_percent = find_max_literacy("M_", "male2", state_code, c08df, c19df)
        female2_grp, female2_percent = find_max_literacy("F_", "female2", state_code, c08df, c19df)
        output2.append([str_state_code, male2_grp, male2_percent, female2_grp, female2_percent])
        
        # Handling one language speakers
        # Here we paass male and female as argument
        # I will assume if to be case of male1
        male1_grp, male1_percent = find_max_literacy("M_", "male", state_code, c08df, c19df)
        female1_grp, female1_percent = find_max_literacy("F_", "female", state_code, c08df, c19df)
        output1.append([str_state_code, male1_grp, male1_percent, female1_grp, female1_percent])
        
        
        
    return output1, output2, output3                
        
            
            

# ---------------------------------------
# Load the Required DF
c19df = get_dataframe_from_excel(filename=c19_file)
c08df = get_dataframe_from_excel(filename=c08_file)
# ---------------------------------------
# Clean the DF

c19df = clean_c19df(c19df)
c08df = clean_c08df(c08df)

output1, output2, output3 = get_literacy_ratio(c08df, c19df)


literacy_lookup = {
    "illiterate":"Illiterate",
    "below_primary":"Literate but below primary",
    "primary":"Primary but below middle",
    "middle":"Middle but below matric/secondary",
    "matric":"Matric/Secondary but below graduate",
    "graduate_and_above":"Graduate and above",
    }

# Updating literacy grp with proper names
for line in output1:
    line[1] = literacy_lookup[line[1]]
    line[3] = literacy_lookup[line[3]]

# Updating literacy grp with proper names
for line in output2:
    line[1] = literacy_lookup[line[1]]
    line[3] = literacy_lookup[line[3]]
    
# Updating literacy grp with proper names
for line in output3:
    line[1] = literacy_lookup[line[1]]
    line[3] = literacy_lookup[line[3]]

header_row = ["state/ut", "literacy-group-males", "ratio-males", 
              "literacy-group-females", "ratio-females"]

write_to_csv(output3, "output/literacy-gender-a.csv", header_row)
write_to_csv(output2, "output/literacy-gender-b.csv", header_row)
write_to_csv(output1, "output/literacy-gender-c.csv", header_row)
