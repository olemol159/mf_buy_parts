import pandas as pd
import pickle
import os

def get_buy_parts(folder_path, buy_parts_path):
    df_buy_parts = pd.read_excel(buy_parts_path, header = 0, usecols="A, K")
    df_buy_parts = df_buy_parts.fillna('')
    df_buy_parts = df_buy_parts.astype(str)
    df_buy_parts = df_buy_parts.replace('', "???")

    with open(os.path.join(folder_path, 'temps', 'df_buy_parts.pkl'), 'wb') as f:
        pickle.dump(df_buy_parts, f)

    return