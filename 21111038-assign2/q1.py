# -*- coding: utf-8 -*-
"""
Created on Sat Oct  9 13:15:37 2021

@author: manjy
"""
import pandas as pd
import csv
csv_file = "dataset/DDW-C18-0000.xlsx"
census_file = "dataset/DDW_PCA0000_2011_Indiastatedist.xlsx"


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
    c18df = c18df[c18df.age_group == "Total"]
    c18df = c18df[c18df.type == "Total"]

    c18df = c18df.drop(["type", "age_group"], axis=1)
    c18df = c18df.drop(["male2", "female2", "male3", "female3"], axis=1)
    # ---------------------------------------
    # Converting to int

    c18df.persons2 = c18df.persons2.astype(int)
    c18df.persons3 = c18df.persons3.astype(int)

    # number of people speaking 2 languages contain
    # 3 languages 2. Using this to extract only
    # Person speaking exactly 2
    c18df.persons2 = c18df.persons2 - c18df.persons3
    #c18df.state_code = c18df.state_code.astype(int)
    #c18df = c18df.set_index("state_code")
    # ---------------------------------------
    # Seperating country and state dataframe
    #country = c18df[c18df.state_code == 0]
    #states = c18df[c18df.state_code != 0]

    #return country, states
    return c18df

def clean_censusdf(censusdf):
    # Selecting only total number
    df = censusdf[censusdf['TRU'] == 'Total']
    # Removing districts
    df = df.loc[df['Level'] != 'DISTRICT']
    # Filtering the required columns
    columns = ["State", "Name", "TOT_P"]
    df = df[columns]
    # Seperating country and state dataframe
    #country_df = df[df.State == 0]
    #states = df[df.State != 0]
    return df


def percent(x, y):
    # Returns x/y percent
    return (x/y)*100


def append_country_percent(country_lang_df, country_census_df, output):
    # Redundant function, not required anymore
    # Coded for debugging.
    # Function to get percentage from country df
    total_pop = country_census_df.TOT_P.values[0]
    exact2 = country_lang_df.persons2.values[0]
    exact3 = country_lang_df.persons3.values[0]
    state_code = country_lang_df.state_code.values[0]

    temp = [state_code, percent(total_pop-exact2-exact3, total_pop),
            percent(exact2, total_pop), percent(exact3, total_pop)]

    output.append(temp)


def append_state_percent(state_lang_df, state_census_df, output):
    
    # Function to get state percentage for each state in list
    # Also gets the country percentage.
    for i in range(len(state_lang_df)):
        # Iterating each row
        # Extracting the required number for percentage
        state_lang_row = state_lang_df.iloc[i]
        state_census_row = state_census_df.iloc[i]
        state_code = state_lang_row.state_code
        total_pop = state_census_row.TOT_P
        exact2 = state_lang_row.persons2
        exact3 = state_lang_row.persons3
        # Storing the percentages in output list
        temp = [state_code, percent(total_pop-exact2-exact3, total_pop),
                percent(exact2, total_pop), percent(exact3, total_pop)]

        output.append(temp)


# ---------------------------------------
# Load the Required DF
c18df = get_dataframe_from_excel(filename=csv_file)
censusdf = get_dataframe_from_excel(filename=census_file)
# ---------------------------------------

# ---------------------------------------
# Clean the DF
lang_df = clean_c18df(c18df)
census_df = clean_censusdf(censusdf)
output = []

# Driver functions
#append_country_percent(country_lang_df, country_census_df, output)
append_state_percent(lang_df, census_df, output)

# WRITE TO CSV
write_to_csv(
    output,
    "output/percent-india.csv",
    ["state-code", "percent-one", "percent-two", "percent-three"]
)
