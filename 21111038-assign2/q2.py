# -*- coding: utf-8 -*-
"""
Created on Sat Oct  9 15:43:56 2021

@author: manjy
"""

import pandas as pd
from scipy.stats import ttest_ind
import csv
csv_file = "dataset/DDW-C18-0000.xlsx"
census_file = "dataset/DDW_PCA0000_2011_Indiastatedist.xlsx"
## UTILS


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
    c18df = c18df.drop(["persons2","persons3"],axis=1)
    #---------------------------------------
    # Converting to int
    
    c18df.male3 = c18df.male3.astype(int)
    c18df.female3 = c18df.female3.astype(int)
    c18df.male2 = c18df.male2.astype(int)
    c18df.female2 = c18df.female2.astype(int)
    
    c18df.male2 = c18df.male2 - c18df.male3
    c18df.female2 = c18df.female2 - c18df.female3
    
    #c18df.state_code = c18df.state_code.astype(int)
    #c18df = c18df.set_index("state_code")
    #---------------------------------------
    
    
    
    return c18df

def clean_censusdf(censusdf):
    df = censusdf[censusdf['TRU'] == 'Total']
    df = df.loc[df['Level'] != 'DISTRICT']
    
    columns = ["State","Name","TOT_M","TOT_F"]
    df = df[columns]
    
    return df

def percent(x, y):
    return (x/y)*100

def get_pvalue(background_vector, ratio_vector):
    _, pvalue = ttest_ind(ratio_vector, background_vector, equal_var=False)
    return pvalue
        

def append_state_percent(state_lang_df, state_census_df):
    output1 = []
    output2 = []
    output3 = []
    for i in range(len(state_lang_df)):
        # Iterating out states
        # Getting desired values and loading in output list
        state_lang_row = state_lang_df.iloc[i]
        state_census_row = state_census_df.iloc[i]
        name = state_lang_row.state_code
        total_popM = state_census_row.TOT_M
        total_popF = state_census_row.TOT_F
        
        exact3M = state_lang_row.male3
        exact3F = state_lang_row.female3
        exact2M = state_lang_row.male2
        exact2F = state_lang_row.female2
        exact1M = total_popM - exact2M - exact3M
        exact1F = total_popF - exact2F - exact3F
        ratio_vector = [exact1M/exact1F,
                    exact2M/exact2F,
                    exact3M/exact3F]
        background_vector = [total_popM/total_popF]*3
        pvalue = get_pvalue(background_vector, ratio_vector)
        
        temp = [name,percent(exact1M,total_popM), percent(exact1F, total_popF), pvalue]
        output1.append(temp)
    
        temp = [name,percent(exact2M,total_popM), percent(exact2F, total_popF), pvalue]
        output2.append(temp)

        temp = [name,percent(exact3M,total_popM), percent(exact3F, total_popF), pvalue]
        output3.append(temp)
    return output1, output2, output3

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

#append_country_percent(country_lang_df, country_census_df, output)

output1, output2, output3 = append_state_percent(state_lang_df, state_census_df)

# WRITE TO CSV
header_row = ["state-code","male-percentage",
"female-percentage", "p-value"]

write_to_csv(output1, "output/gender-india-a.csv", header_row)
write_to_csv(output2, "output/gender-india-b.csv", header_row)
write_to_csv(output3, "output/gender-india-c.csv", header_row)