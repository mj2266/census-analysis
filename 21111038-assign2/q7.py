# -*- coding: utf-8 -*-
"""
Created on Thu Oct 14 12:07:41 2021

@author: manjy
"""



import os
import pandas as pd
import csv
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

def merge_df(target_df, df):
    # Merges rows of the df to target df.
    df = df.dropna()
    df.columns = ["lang","person"]
    target_df = target_df.append(df)
    
    return target_df
    

def append_languages(target_df, csv_file, one_col=False):
    # There will be empty df,
    # and a list of csv files
    # We need to make one final df, with values from these csvs
    # merged into one df
    # Code behave differently, on whether we want values from
    # only one column(mothertongue) or all3 values
    state_df = get_dataframe_from_excel(csv_file)
    
    state_df = state_df.rename(
                    columns={"Unnamed: 3":"lang1", "Unnamed: 4":"person1",
                    "Unnamed: 8":"lang2", "Unnamed: 9":"person2",
                    "Unnamed: 13":"lang3", "Unnamed: 14":"person3",})
    columns = ["lang1","person1","lang2","person2","lang3","person3"]
    state_df = state_df[columns]
    state_df = state_df.drop([0,1,2,3])
    if one_col:
        lang1_df = state_df[["lang1", "person1"]]
        target_df = merge_df(target_df, lang1_df)
    else:
        lang1_df = state_df[["lang1", "person1"]]
        lang2_df = state_df[["lang2", "person2"]]
        lang3_df = state_df[["lang3", "person3"]]
        target_df = merge_df(target_df, lang1_df)
        target_df = merge_df(target_df, lang2_df)
        target_df = merge_df(target_df, lang3_df)
        
    return target_df


def handle_region(region, one_col=False):
    
    #----------------------------------------------
    # Adding csv files name of region in list
    csv_list = os.listdir(f"dataset/q7dataset/{region}")
    csv_list = [f"dataset/q7dataset/{region}/{x}" for x in csv_list]
    #----------------------------------------------
    # Creating empty DF and we will append total counts 
    # in this DF
    final_df = pd.DataFrame(columns=["lang","person"])
    #----------------------------------------------
    # updating the final df with all csv values
    for csv_file in csv_list:
        if one_col:
            final_df = append_languages(final_df, csv_file, one_col=True)
        else:
            final_df = append_languages(final_df, csv_file)
    
    # Grouping to get single value
    final_df.person = final_df.person.astype(int)
    final_df = final_df.groupby("lang").sum().reset_index()
    final_df = final_df.sort_values(by="person", ascending=False)
    return final_df
    


regions = ["North", "West", "Central","East","South","North-East"]



output = []

# CASE ALL 3 COLUMNS USED
for region in regions:
    # Iterating over all regions and getting their outputs.
    # Finding max 3 regions for them
    # This is case for when using all three columns
    out1 = handle_region(region)
    out1Top3 = out1.head(3).lang.tolist()
    output.append([region]+out1Top3)

output_df = pd.DataFrame(output, columns =["region","language-1","language-2","language-3"])
output.sort()
header_row = ["region", "language-1", "language-2", "language-3"]
write_to_csv(output, "output/region-india-b.csv", header_row)

# CASE ONLY MOTHER LANGUAGE COLUMN USED
output_one_col = []

for region in regions:
    
    out1 = handle_region(region, one_col=True)
    out1Top3 = out1.head(3).lang.tolist()
    output_one_col.append([region]+out1Top3)
output_one_col_df = pd.DataFrame(output_one_col, columns =["region","language-1","language-2","language-3"])
output_one_col.sort()
write_to_csv(output_one_col, "output/region-india-a.csv", header_row)

