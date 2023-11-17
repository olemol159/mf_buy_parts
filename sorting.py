import numpy as np
import pandas as pd
import pickle
import os

def get_df_rozpiska(file_path, folder_path):
    df_rozpiska = pd.read_excel(file_path)
    # nrows = df_rozpiska.shape[0]     # df.shape[0] - pocet riadkov v DataFrame

    #------------------------------ lokalizacia BG_ARTIKELNR pozicie ----------------------------------
    target_value = "BG_ARTIKELNR"

    # Filter the DataFrame to find the position of the target_value
    mask = df_rozpiska.eq(target_value)
    row_index, column_index = mask.values.nonzero()
    row_index = row_index[0]  # In case there are multiple occurrences, take the first one
    column_index = column_index[0]  # In case there are multiple occurrences, take the first one

    #--------------------------------------------------------------------------------------------------

    df_rozpiska = pd.read_excel(file_path,
        header = row_index + 1, 
        sheet_name = 0,
        # skiprows = [3] # + list(range(417, df_rozpiska.shape[0]))   
    )

    df_rozpiska.insert(df_rozpiska.columns.get_loc("Drawing Revision"), "OVL Numbers", value=np.nan)  # vloží stlpec prazdnych hodnot

    df_rozpiska = df_rozpiska.fillna("")  # odstrani NaN vyrazy, použiť ešte pre funkciou odstránenia .0 v ZEICHNUNG-e


    # df = df.astype({'Art':'string','ZEICHNUNG':'string'}) # vybrané stĺpce na stringy
    # df_string = df.astype(str) # vsetko stringy
    df_rozpiska = df_rozpiska.astype({
        'STRU_EBENE':'str',
        'STKL_BEZUG':'str',
        'BDE_NR':'str',
        'BG_ARTIKELNR':'str',
        "Art":"str",
        "ZEICH_POSN":"int",
        "ARTIKEL":"str",
        "ZEICHNUNG":"str",           
        # "Stĺpec1"             float64
        "Drawing Revision":'str',
        "MENGE_GES":'str',
        "MENGE":'str'
        # "ME"                   object
        # "BEZEICH":"str", 
        # "MEMO_TECH"            object
        # "MEMO_VERTR"           object
        # "Drawing size"         object
        # "Drawing Scale"
        })

    df_rozpiska.replace(r'\n', '', regex=True, inplace=True)
    df_rozpiska = df_rozpiska.applymap(lambda x: x.strip() if isinstance(x, str) else x)

    # ---------------------------------------------------------------------------
    # funkcia pre odstranénie .0 na koncí v stringoch
    def remove_trailing_zero(value):
        if isinstance(value, str) and value != "":
            if value.endswith(".0"):
                return value[:-2]
        return value
    
    df_rozpiska['STRU_EBENE'] = df_rozpiska['STRU_EBENE'].apply(remove_trailing_zero)
    df_rozpiska['STKL_BEZUG'] = df_rozpiska['STKL_BEZUG'].apply(remove_trailing_zero)
    df_rozpiska['BDE_NR'] = df_rozpiska['BDE_NR'].apply(remove_trailing_zero)
    df_rozpiska['ZEICHNUNG'] = df_rozpiska['ZEICHNUNG'].apply(remove_trailing_zero)   # vo všetkych výrazy, ktoré obsahuju .0 na konci vymaže .0
    df_rozpiska['ARTIKEL'] = df_rozpiska['ARTIKEL'].apply(remove_trailing_zero)
    df_rozpiska['BG_ARTIKELNR'] = df_rozpiska['BG_ARTIKELNR'].apply(remove_trailing_zero)
    df_rozpiska['MENGE'] = df_rozpiska['MENGE'].apply(remove_trailing_zero)
    df_rozpiska['MENGE_GES'] = df_rozpiska['MENGE_GES'].apply(remove_trailing_zero)
    # ---------------------------------------------------------------------------

    df_rozpiska['Drawing Revision'] = df_rozpiska['Drawing Revision'].apply(remove_trailing_zero)
    def add_zero(x):
        if len(x) == 1:
            return "0" + x
        return x
    df_rozpiska['Drawing Revision'] = df_rozpiska['Drawing Revision'].apply(add_zero)

    df_rozpiska = df_rozpiska[~df_rozpiska['BEZEICH'].str.contains(".*\+\+\+.*")]  # ak v BEZEICH sa nachádza poznámka +++text+++ vymaže/preskočí riadok

    df_rozpiska['BG_ARTIKELNR'] = df_rozpiska['BG_ARTIKELNR'].str.strip()
    df_rozpiska['ZEICHNUNG'] = df_rozpiska['ZEICHNUNG'].str.strip()
    # Convert "MENGE" column to float
    df_rozpiska['MENGE'] = pd.to_numeric(df_rozpiska['MENGE'], errors='coerce')

    # Convert "MENGE_GES" column to float
    df_rozpiska['MENGE_GES'] = pd.to_numeric(df_rozpiska['MENGE_GES'], errors='coerce')

    # ---------------------------------------------------------------------------
    # vydelenie množstva kusov BG
    # iterate through rows and update values
    # OšETRENIE PRVéHO RIADKU ABY FUNGOVAL CYKLUS  
    empty_bg_indices = df_rozpiska[df_rozpiska['BG_ARTIKELNR'].eq('')].index
    if not empty_bg_indices.empty:
        df_rozpiska.loc[empty_bg_indices[0], 'BG_ARTIKELNR'] = 1

    for index, row in df_rozpiska.iterrows():
        if row['MENGE'] == '' or pd.isna(row['MENGE']):
            a = row['MENGE_GES'] 
            b = 1
            while True:
                c = df_rozpiska.loc[(df_rozpiska['ZEICHNUNG'] == row['BG_ARTIKELNR'])
                                    & (df_rozpiska.index != index),
                                    'MENGE_GES']
                if not c.empty:
                    c = c.reset_index(drop=True)  # reset the index to remove any duplicates
                    c_value = c.iloc[0]  # get the first value in the c Series
                    b = b * c_value
                    # update row to refer to the matching row
                    matching_index = c.index[0]
                    row = df_rozpiska.loc[matching_index]
                else:
                    break
            df_rozpiska.at[index, 'MENGE'] = str(a // b)

    # ---------------------------------------------------------------------------
    # ošetrenie chýbajúcich revizí a referenciína revízie
    for index, row in df_rozpiska.iterrows():
        if (not (row['ZEICHNUNG'] == '' or pd.isna(row['ZEICHNUNG']))) & (row['Drawing Revision'] == '' or pd.isna(row['Drawing Revision'])):
            df_rozpiska.at[index, 'Drawing Revision'] = 'NOT REV'
    # ---------------------------------------------------------------------------

    df_rozpiska['MENGE_GES'] = df_rozpiska['MENGE_GES'].apply(remove_trailing_zero)
    df_rozpiska = df_rozpiska.drop(columns=['MENGE_GES'])
    df_rozpiska['MENGE'] = df_rozpiska['MENGE'].astype(str)
    df_rozpiska['MENGE'] = df_rozpiska['MENGE'].apply(remove_trailing_zero)

 
    if not os.path.exists(os.path.join(folder_path, 'temps')):
        os.makedirs(os.path.join(folder_path, 'temps'))

    with open(os.path.join(folder_path, 'temps', 'df_rozpiska_no_ovl.pkl'), 'wb') as f:
        pickle.dump(df_rozpiska, f)
    


