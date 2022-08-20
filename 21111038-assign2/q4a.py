# -*- coding: utf-8 -*-
"""
Created on Sat Oct  9 16:18:31 2021

@author: manjy
"""

import pandas as pd
import csv
csv_file = "dataset/DDW-C18-0000.xlsx"
census_file = "dataset/DDW_PCA0000_2011_Indiastatedist.xlsx"
## UTILS


def get_dataframe_from_excel(filename):
    # read excel
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
            write.writerow([row[0]])


## END


def clean_c18df(c18df):
    #---------------------------------------
    # Renaming the columns
    
    columns = ["state_code","district_code", "area_name",
               "type", "age_group","persons2","male2","female2",
               "persons3","male3","female3"]
    
    c18df.columns = columns
    #---------------------------------------
    # Filtering to get only Total data,
    # And dropping useless columns
    
    c18df = c18df.drop(["district_code"],axis=1)
    c18df = c18df[c18df.age_group == "Total"]
    c18df = c18df[c18df.type == "Total"]
    
    c18df = c18df.drop(["type","age_group"],axis=1)
    c18df = c18df.drop(["male2","female2","male3","female3"],axis=1)
    #---------------------------------------
    # Converting to int
    
    c18df.persons2 = c18df.persons2.astype(int)
    c18df.persons3 = c18df.persons3.astype(int)
    
    # number of people speaking 2 languages contain
    # 3 languages 2. Using this to extract only 
    # Person speaking exactly 2
    c18df.persons2 = c18df.persons2 - c18df.persons3
    #c18df.state_code = c18df.state_code.astype(int)
    #c18df = c18df.set_index("state_code")
    #---------------------------------------
    
    states = c18df[c18df.state_code != "00"]
    
    return states

def clean_censusdf(censusdf):
    # Filtering out useless rows
    df = censusdf[censusdf['TRU'] == 'Total']
    # filtering out district entries
    df = df.loc[df['Level'] != 'DISTRICT']
    # Extracting desired columns
    columns = ["State","Name","TOT_P"]
    df = df[columns]
    # Extracting state entries
    states = df[df.State != 0]
    return states

def percent(x, y):
    # Simple percentage function x/y.
    return (x/y)*100
    

def append_state_percent(state_lang_df, state_census_df, output, type="32"):
    # This function calculates for all states
    for i in range(len(state_lang_df)):
        # iterating for each state
        state_lang_row = state_lang_df.iloc[i]
        state_census_row = state_census_df.iloc[i]
        name = state_lang_row.state_code
        total_pop = state_census_row.TOT_P
        exact2 = state_lang_row.persons2
        exact3 = state_lang_row.persons3
        exact1 = total_pop - exact3 - exact2
        
        # Type 32 means ratio 3:2,
        # Type 21 means ratio of 2:1
        # Depending on type, we append the data to output.
        if type == "32":
            temp = [name, 
                    percent(exact3,total_pop) / percent(exact2,total_pop)]
        
        elif type =="21":
            temp = [name, 
                    percent(exact2,total_pop) / percent(exact1,total_pop)]
        
        output.append(temp)

#---------------------------------------
# Load the Required DF
c18df = get_dataframe_from_excel(filename=csv_file)
censusdf = get_dataframe_from_excel(filename=census_file)
#---------------------------------------

#---------------------------------------
# Clean the DF
state_lang_df = clean_c18df(c18df)
del(c18df)
state_census_df = clean_censusdf(censusdf)
del(censusdf)
output = []

append_state_percent(state_lang_df, state_census_df, output)

output.sort(key=lambda x:x[-1])
lower_ratio32 = output[0:3]
higher_ratio32 = output[-3:]
higher_ratio32.reverse()



# 
# WRITE TO CSV HIGHERR RATIO, THEN LOWER RATIO
header_row = ["state/ut"]
write_to_csv(higher_ratio32+lower_ratio32, "output/3-to-2-ratio.csv", header_row)