import pandas as pd
import pickle
import os

def bom_creation_tool(folder_path):
    with open(os.path.join(folder_path, 'temps', 'df_rozpiska.pkl'), 'rb') as f:
        df_rozpiska = pickle.load(f)


    df_rozpiska['BDE_NR'] = df_rozpiska['BDE_NR'].astype(str)
    df_rozpiska['ZEICHNUNG'] = df_rozpiska['ZEICHNUNG'].astype(str)
    df_rozpiska['BG_ARTIKELNR'] = df_rozpiska['BG_ARTIKELNR'].astype(str)

    main_subassy_all_col_df = df_rozpiska[
        (df_rozpiska['STRU_EBENE'] == '1') &
        (df_rozpiska['STKL_BEZUG'] == '0') &
        ~((df_rozpiska['ZEICHNUNG'] == '') | pd.isna(df_rozpiska['ZEICHNUNG']))
        ]


    def expand_rows(start_row, df_rozpiska, level=0):
        expanded_rows = [start_row.to_dict()]

        # Find rows in df_rozpiska based on conditions
        matching_rows = df_rozpiska[
            (df_rozpiska['BG_ARTIKELNR'] == start_row['ZEICHNUNG']) &
            (df_rozpiska['STKL_BEZUG'] == start_row['BDE_NR'])
        ]
        
        if not matching_rows.empty:
            level += 1
            for _, row in matching_rows.iterrows():
                expanded_rows.extend(expand_rows(row, df_rozpiska, level))

        return expanded_rows
    
    if not os.path.exists(os.path.join(folder_path, 'temp')):
        os.makedirs(os.path.join(folder_path, 'temp'))

    for index, row in main_subassy_all_col_df.iterrows():
        ms_zeich = row['ZEICHNUNG']
        result_df = expand_rows(row, df_rozpiska)
           
        pkl_path = os.path.join(folder_path, 'temp', f"{ms_zeich}.pkl")
        pd.DataFrame(result_df).to_pickle(pkl_path)

