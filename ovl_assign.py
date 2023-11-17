import pickle
import os
import pandas as pd 

def get_assign(folder_path):
    with open(os.path.join(folder_path, 'temps', 'df_rozpiska_no_ovl.pkl'), 'rb') as f:
        df_rozpiska_no_ovl = pickle.load(f)
    with open(os.path.join(folder_path, 'temps', 'df_buy_parts.pkl'), 'rb') as f:
        df_buy_parts = pickle.load(f)    

    grouped = df_buy_parts.groupby('ARTIKEL')['OVL#NUMBER'].apply(list)     # Group the rows in df_buy_parts by 'ARTIKEL' and create a list of corresponding 'OVL#NUMBER' values
    df_rozpiska_no_ovl['OVL Numbers'] = df_rozpiska_no_ovl['ARTIKEL'].map(grouped).fillna('')  # Update the 'OVL Numbers' column in df_rozpiska with the corresponding list of values from grouped
    df_rozpiska_no_ovl['OVL Numbers'] = df_rozpiska_no_ovl['OVL Numbers'].apply(lambda x: ''.join(x)) # Concatenate the strings in each list in the 'OVL Numbers' column into a single string
    df_rozpiska_ovl = df_rozpiska_no_ovl

    for index, row in df_rozpiska_ovl.iterrows():
        if (row['OVL Numbers'] == '' or pd.isna(row['OVL Numbers'])) & (row['ZEICHNUNG'] == '' or pd.isna(row['ZEICHNUNG'])):
            df_rozpiska_ovl.at[index, 'OVL Numbers'] = '???'

    os.remove(os.path.join(folder_path, 'temps', 'df_buy_parts.pkl'))
    os.remove(os.path.join(folder_path, 'temps', 'df_rozpiska_no_ovl.pkl'))

    # vytvorí pomocný súbor pre samotné vytvorenie rozpisky 
    with open(os.path.join(folder_path, 'temps', 'df_rozpiska.pkl'), 'wb') as f:
        pickle.dump(df_rozpiska_ovl, f)
    
    # df_rozpiska_ovl.to_csv('output.csv', index=False)
