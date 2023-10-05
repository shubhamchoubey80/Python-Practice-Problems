import pandas as pd
import numpy as np
import argparse

import glob

parser = argparse.ArgumentParser(description="Process some data file")
parser.add_argument('--fp', type=str, help='Data to be processed')
parser.add_argument('--sfp', type=str, help='Data to be processed')
args = parser.parse_args()

File_path = args.fp
Status_file_path = args.sfp
all_data = pd.DataFrame()

def data_comb(File_path,Status_file_path):
    glob.glob(File_path)
    for f in glob.glob(File_path):
        df = pd.read_excel(f)
        all_data = all_data.append(df,ignore_index=True)
   
    all_data['date'] = pd.to_datetime(all_data['date'])

    status = pd.read_excel(Status_file_path)

    all_data_st = pd.merge(all_data, status, how='left')

    all_data_st['status'].fillna('bronze',inplace=True)

    all_data_st["status"] = all_data_st["status"].astype("category")
    all_data_st.dtypes

    all_data_st.groupby(["status"])["quantity","unit price","ext price"].mean()

    all_data_st.groupby(["status"])["quantity","unit price","ext price"].agg([np.sum,np.mean, np.std])

    all_data_st.drop_duplicates(subset=["account number","name"]).ix[:,[0,1,7]].groupby(["status"])["name"].count()

    print(all_data_st)

if File_path != None and Status_file_path != None:
   data_comb(File_path,Status_file_path)

print(all_data_st)