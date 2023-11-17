import json
import os
import pickle
import pandas as pd

def bom_renaiming(folder_path,  erzeugnis_json_path, width_variant, project_number):
    # Read JSON data from a file

    def as_string(obj):
        """Convert all values to strings."""
        if isinstance(obj, (int, float)):
            return str(obj)
        elif isinstance(obj, list):
            return [as_string(item) for item in obj]
        elif isinstance(obj, dict):
            return {key: as_string(value) for key, value in obj.items()}
        else:
            return obj
    
    with open(erzeugnis_json_path, 'r', encoding='utf-8') as file:
        data_list = json.load(file, object_hook=as_string)


    help_assy_list= os.listdir(os.path.join(folder_path, 'temp'))

    for hal in help_assy_list:
        file_path = os.path.join(folder_path, 'temp', hal)

        with open(file_path, 'rb') as file:  # Open the file in binary mode
            bom_list = pickle.load(file)
        
        # if os.path.exists(file_path):
        #     os.remove(file_path)

        # -------------------------------- width variant added --------------------------------
        for index, row in bom_list.iterrows():
            if row['Art'] == 'BG':
                # Check if the condition is met
                condition_sub_assy_list = (bom_list['BG_ARTIKELNR'] == row['ZEICHNUNG']) & (bom_list['STKL_BEZUG'] == row['BDE_NR'])

                # Use the condition to filter the DataFrame
                different_part_number = bom_list[condition_sub_assy_list]
            
                for i_dpn, r_dpn in different_part_number.iterrows():
                    if r_dpn['ZEICHNUNG'].strip():  # Check if the string is empty after stripping whitespaces
                        if r_dpn['ZEICHNUNG'] != r_dpn['ARTIKEL']:
                            bom_list.at[index, 'ARTIKEL'] += '-' + width_variant
                            break

        # --------------------------------------------------------------------------------------
            
        # ----------------------- ARTIKEL - BEZICH of 1st row changed ---------------------------
        for index, row in bom_list.iterrows():
            if row['STRU_EBENE'] == '1':
                zeichnung_key = row['ZEICHNUNG']
                        
                # Search for the item in data_list where 'Drawing' matches zeichnung_key
                matching_items = [item_zeichnung for item_zeichnung in data_list if item_zeichnung.get('Drawing') == zeichnung_key]

                # Check if any matching item is found
                if matching_items:
                    note_value = matching_items[0].get('Note', '')

                    # Check if 'Note' is present before updating columns
                    if note_value:
                        bom_list.at[index, 'ARTIKEL'] = str(note_value) + ' AB' + width_variant + '-' + project_number
                        bom_list.at[index, 'BEZEICH'] += ' AB' + width_variant + '-' + project_number
                    
        # --------------------------------------------------------------------------------------

        # ---------------------------------- rename columns --------------------------------------

        bom_list = bom_list.rename(columns={'ZEICH_POSN': 'POS', 
                                        'Drawing Revision': 'DRW REV',
                                        'Drawing size': 'DRW FOR', 
                                        'STRU_EBENE': 'EB'})


        # --------------------------------------------------------------------------------------

        with open(file_path, 'wb') as f:
            pickle.dump(bom_list, f)
        
        # bom_list.to_csv(os.path.join(folder_path, ' rename_output.csv'),index=False)

