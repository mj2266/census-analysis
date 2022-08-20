
Make a virtual environment to run this code.(NOTE:   Creating virtual environment is optional, you can go to direct 
                                                        step 4 instead, but its recommended to use virtual environment)
    Example on how to make it on ubuntu 18.04:
        1)sudo apt-get install python3-venv
        2) inside the project folder execute following command:
            python3 -m venv venv

        3) now execute : 
            source venv/bin/activate

        4) Install all the required packages:
            pip install -r requirements.txt

Important packages Used: 
- numpy
- pandas 
- openpyxl

Complete list of packages is avaiable in requirements.txt
================================================================================================

Give execution permission to the sh files:

Type following command in the main code folder. 

find ./ -type f -iname "*.sh" -exec chmod +x {} \;

================================================================================================

assign2.sh is the top level script which executes all the programs.

Question 1)
- input files:  - dataset/DDW-C18-0000.xlsx
                - dataset/DDW_PCA0000_2011_Indiastatedist.xlsx
- sh script: percent-india.sh
- source code: q1.py
- output path: output/percent-india.csv

- Census file is used to get data for people speaking only 1 language. 
  This method will be implicitly used in question coming ahead too
- Column name "Number speaking second language" for file C18 includes people speaking 3 or more languages too.
- This has been handled to get speakers that speak only 2 languages.
- Similar assumption is to be implied when using c18 or c19 files in upcoming questions.

================================================================================================
Question 2)
- input files: 
                - dataset/DDW-C18-0000.xlsx
                - dataset/DDW_PCA0000_2011_Indiastatedist.xlsx
- sh script: gender-india.sh
- source code: q2.py
- output path: 
                - output/gender-india-a.csv
                - output/gender-india-b.csv
                - output/gender-india-c.csv

- To find significance difference between male ratio is to female,
  we have used t-test.
- We have made background vector, which consists of 3 elements repeated thrice, which contains
  ratio of total number of male: total number of female
- And our actual vector will have 3 elements: male speaking 1 language/ female speaking 1 language, 
  male speaking 2 language/ female speaking 2 language, male speaking 3 language/ female speaking 3 language   
- Pvalue is found by using t-test on these 2 vectors.
- For Null Hypothesis, we will have that there is no significant difference between male to female
- Thus alternate hypothesis will be that theres significant difference
- We will have threshold alpha = 0.05, if pvalue < alpha, we reject null hypothesis
- For non of the states, we got p-value less than alpha, so for all states, we accept the null hypothesis

================================================================================================
Question 3)
- input files:  
                - dataset/DDW-C18-0000.xlsx
                - dataset/DDW_PCA0000_2011_Indiastatedist.xlsx
- sh script: geography-india.sh
- source code: q3.py
- output path:  
                - output/geography-india-a.csv
                - output/geography-india-b.csv
                - output/geography-india-c.csv

- To find significance difference between urban ratio is to rural,
  we have used t-test.
- We have made background vector, which consists of 3 elements repeated thrice, which contains
  ratio of total number of urban people : total number of rural people
- And our actual vector will have 3 elements: urban people speaking 1 language/ rural people speaking 1 language, 
  urban people speaking 2 language/ rural people speaking 2 language, 
  urban people speaking 3 language/ rural people speaking 3 language   
- Pvalue is found by using t-test on these 2 vectors.
- For Null Hypothesis, we will have that there is no significant difference between urban people to rural people
- Thus alternate hypothesis will be that theres significant difference
- We will have threshold alpha = 0.05, if pvalue < alpha, we reject null hypothesis
- For non of the states, we got p-value less than alpha, so for all states, we accept the null hypothesis

================================================================================================

Question 4)
- input files:  
                - dataset/DDW-C18-0000.xlsx
                - dataset/DDW_PCA0000_2011_Indiastatedist.xlsx

- sh file:   
            - 3-to-2-ratio.sh
            - 2-to-1-ratio.sh
          
- source code: q4a.py, q4b.py
- output path:  
                - output/3-to-2-ratio.csv
                - output/2-to-1-ratio.csv

- The output file contains 7 rows(1 row header+ 6 row output), and 2 columns(state_code, ratio)
- first 3 output rows contains top 3 states of the specified ratio in higher to lower ratio order
- next 3 output rows contains worst 3 states of the specified ratio in lower to higher ratio order
- There are 2 output files, one contains ratio of 3 language is to 2 language speakers
  other contains 2 language is to 1 language speakers.
- Source code to generate 3:2 ratio is in q4a.py, and source code for 2:1 is in q4b.py

================================================================================================

Question 5)
- input files: 
              - dataset/DDW-C18-0000.xlsx
              - dataset/DDW-0000C-14.xls

- sh script: age-india.sh
- source code: q5.py
- output path:  age-india.csv

- Age groups from c14 have been merged
  Finer age groups between 30-49(i.e 30-34, 35-39..) have been merged into 30-49 to match with c18 data.
  Finer age groups from 50-69 are also merged.
  Finer Age groups above 70 are merged into 70+ age group.
- Thus age groups used are 5-9, ,10-14, 15-19, 20-24, 25-29, 30-49, 50-69, 70+
- Age group mentioned 0-4 and "Age not stated" are ignored.

================================================================================================

Question 6)
- input files:  
                - dataset/DDW-C19-0000.xlsx
                - dataset/DDW-0000C-08.xlsx
- sh script: literacy-india.sh
- source code: q6.py
- output path: output/literacy-india.csv

- Literacy group "literate" is subdivided, so we wont be considering the "literacy" as a group
- From C08 file, Matric/Secondary, Higer Secondary, Non-Technical Diploma, Technical Diploma are merged 
  together to group "Matric/Secondary but below graduate".
- This is because there is finer division in C08 file.
================================================================================================

Question 7)
- input folder: dataset/q7dataset/*
- sh script: region-india.sh
- source code: q7.py
- output path: 
                - output/region-india-a.csv
                - output/region-india-b.csv

- c17 files for each state, and UT is inside the folder q7/
- They are segregated according to their region.
- This is done so that coding effort is decreased by adding loops.
- Ignoring recently formed states and UT Telangana, Ladakh because they weren't there seperately in census 2011.

================================================================================================

Question 8)
- input files:  
                - dataset/DDW-C18-0000.xlsx
                - dataset/DDW-0000C-14.xls
- sh script: age-gender.sh
- source code: q8.py
- output path:
                - output/age-gender-a.csv
                - output/age-gender-b.csv
                - output/age-gender-c.csv

- Age groups from c14 have been merged
  Finer age groups between 30-49(i.e 30-34, 35-39..) have been merged into 30-49 to match with c18 data.
  Finer age groups from 50-69 are also merged.
  Finer Age groups above 70 are merged into 70+ age group.
- Thus age groups used are 5-9, ,10-14, 15-19, 20-24, 25-29, 30-49, 50-69, 70+
- Age group mentioned 0-4 and "Age not stated" are ignored.


================================================================================================

Question 9)
- input files: 
                - dataset/DDW-C19-0000.xlsx
                - dataset/DDW-0000C-08.xlsx
- sh script: literacy-gender.sh
- source code: q9.py
- output path: 
                - output/literacy-gender-a.csv
                - output/literacy-gender-b.csv
                - output/literacy-gender-c.csv

- Literacy group "literate" is subdivided, so we wont be considering the "literacy" as a group
- From C08 file, Matric/Secondary, Higer Secondary, Non-Technical Diploma, Technical Diploma are merged 
  together to group "Matric/Secondary but below graduate".
- This is because there is finer division in C08 file.