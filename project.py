#! /usr/bin/python

#sat3310 - final project
#created by agtoyli@mtu.edu
#due 4/15/26

#import modules
import requests
import os
import pandas as pd
import subprocess

#define variables
debug = True
dataPath = "/home/sat3310/Documents/project/data/"
dataFile = "No file name specified"
dataUrl = "No URL specified"
rPath = "/home/sat3310/Documents/project/rDir/"
rFile = "project.R"
rOut = "eda_output.txt"
catVars = list()
numVars = list()

#get data source
dataUrl = input("Please paste URL of data you would like to download: ")
#check that url was entered correctly
if debug:
    print(dataUrl)
#specify file name
dataFile = input("Please input the local name for your datafile: ")
if debug:
    print(dataFile)

#download data
if debug:
    print(f"Downloading data from {dataUrl}...")
response = requests.get(dataUrl)

#check status code and write local file if successful
if response.status_code == 200:
    with open(dataPath+dataFile, 'wb') as file:
        file.write(response.content)
    print(f"File successfully saved to: {dataPath+dataFile}")
#print status code if request was unsuccessful
else:
    print(f"Error: Could not download file. Status code: {response.status_code}")

#read header and present variables to user
fileHead = pd.read_csv(dataPath+dataFile, nrows=5)
print(fileHead.info())

#have user select categorical variables
print("Enter the indices of the categorical variables you would like to explore. Press enter after each index number and 'x' to finish.")
while(1>0):
    var = input("Index: ")
    if var == "x":
        break
    else:
        catVars.append(fileHead.columns[int(var)])
#flatten list
catVars_str = ",".join(catVars)
#print variable names for debugging
if debug:
    print(catVars_str)

#have user select numeric variables
print("Enter the indices of the numeric variables you would like to explore. Press enter after each index number and 'x' to finish.")
while(1>0):
    var = input("Index: ")
    if var == "x":
        break
    else:
        numVars.append(fileHead.columns[int(var)])
#flatten list
numVars_str = ",".join(numVars)
#print variable names for debugging
if debug:
    print(numVars_str)

# Construct the R command
# format: Rscript scriptname.R arg1 arg2 arg3
cmd = ["Rscript", rPath+rFile, rPath, dataPath+dataFile, catVars_str, numVars_str]
#print command
if debug:
    print(f"Executing: {' '.join(cmd)}")

# define path for R output file
log_file_path = os.path.join(rPath, rOut)

#run script and and write r results to file
try:
    #open the output file
    with open(log_file_path, "w") as log_file:
        print(f"Running R script... logging to {log_file_path}")
        
        #pass the file handle to stdout and stderr
        result = subprocess.run(
            cmd, 
            check=True, 
            stdout=log_file, 
            stderr=log_file, 
            text=True
        )
    print("R Script completed successfully.")

#handle errors
except subprocess.CalledProcessError as e:
    print(f"R Script failed. Check the log file at: {log_file_path}")

#done
