# -*- coding: utf-8 -*-
"""
Created on Sat Oct  9 18:08:25 2021

@author: manjy
"""

import pandas as pd
from scipy.stats import chisquare,ttest_ind
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
    c18df = c18df[ c18df.type.isin(["Rural","Urban"]) ]
    
    c18df = c18df.drop(["age_group"],axis=1)
    c18df = c18df.drop(["male2","female2","male3","female3"],axis=1)
    #---------------------------------------
    # Converting to int
    
    c18df.persons3 = c18df.persons3.astype(int)
    c18df.persons2 = c18df.persons2.astype(int)
    c18df.persons2 = c18df.persons2 - c18df.persons3
    
    #c18df.state_code = c18df.state_code.astype(int)
    #c18df = c18df.set_index("state_code")
    #---------------------------------------
    
    
    return c18df

def clean_censusdf(censusdf):
    df = censusdf[censusdf['TRU'].isin(["Rural","Urban"])]
    df = df.loc[df['Level'] != 'DISTRICT']
    
    columns = ["State","Name","TRU","TOT_P"]
    df = df[columns]

    return df

def percent(x, y):
    return (x/y)*100

def get_pvalue(background_vector, ratio_vector):
    _, pvalue = ttest_ind(ratio_vector, background_vector, equal_var=False)
    return pvalue


        

def append_state_percent(state_lang_df, state_census_df):
    
    rural_df = state_lang_df[state_lang_df.type=="Rural"]
    urban_df = state_lang_df[state_lang_df.type=="Urban"]
    rural_census_df = state_census_df[state_census_df.TRU =="Rural"]
    urban_census_df = state_census_df[state_census_df.TRU =="Urban"]
    
    output1 = []
    output2 = []
    output3 = []
    
    for i in range(len(rural_df)):
        # Iterating out states
        # Getting desired values and loading in output list
        rural_row = rural_df.iloc[i]
        urban_row = urban_df.iloc[i]
        rural_census_row = rural_census_df.iloc[i]
        urban_census_row = urban_census_df.iloc[i]
        
        name = rural_row.state_code
        total_pop_rural = rural_census_row.TOT_P
        total_pop_urban = urban_census_row.TOT_P
        
        exact3U = urban_row.persons3
        exact3R = rural_row.persons3
        exact2U = urban_row.persons2
        exact2R = rural_row.persons2
        exact1U = total_pop_urban - exact2U - exact3U
        exact1R = total_pop_rural - exact2R - exact3R
       
        ratio_vector = [exact1U/exact1R, exact2U/exact2R, exact3U/exact3R]
        background_vector = [total_pop_urban/total_pop_rural]*3
        
        pvalue = get_pvalue(background_vector, ratio_vector)
        

        temp = [name, percent(exact1U,total_pop_urban), percent(exact1R, total_pop_rural), pvalue]
        output1.append(temp)
        
        temp = [name, percent(exact2U,total_pop_urban), percent(exact2R, total_pop_rural), pvalue]
        output2.append(temp)

        temp = [name, percent(exact3U,total_pop_urban), percent(exact3R, total_pop_rural), pvalue]
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
header_row = ["state-code","urban-percentage", "rural-percentage",
"p-value"]

write_to_csv(output1, "output/geography-india-a.csv", header_row)
write_to_csv(output2, "output/geography-india-b.csv", header_row)
write_to_csv(output3, "output/geography-india-c.csv", header_row)   


