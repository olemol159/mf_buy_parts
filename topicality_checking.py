import pandas as pd
import pickle
import os
import PyPDF2
 
import eofn2

#------------------------------------------------------------------------------------------------
def checking_tool(folder_path, path_PDF, path_STEP):
    # print(path_PDF, path_STEP)
    df_list_of_PDF, df_list_of_STEP = eofn2.get_dataframes(path_PDF, path_STEP)     # vytvorí dataframes z priečinkov na serveri, kde sú STEP a PDF súbory 
    storage_df = pd.DataFrame(columns=['ARTIKEL', 'Drawing Revision']) #for STEPs missing
    help_assy_list= os.listdir(os.path.join(folder_path, 'temp'))

    for hal in help_assy_list:
        file_path = os.path.join(folder_path, 'temp', hal)

        with open(file_path, 'rb') as file: # nahrá iterovanú rozpisku
            bom_list = pickle.load(file)
        # if os.path.exists(file_path):   # po vytvorení rozpisky odstráni pomocný súbor
        #     os.remove(file_path)

        bom_list = bom_list[(bom_list['ZEICHNUNG'].str.strip() != '') & (bom_list['Drawing Revision'].str.strip() != '')]       # remove rows where either 'ZEICHNUNG' or 'Drawing Revision' is empty or whitespace
        #------------------------------------------------------------------------------------




        #------------------------------------------------------------------------------------
        # KONTORLA AKTUALNOSTI PDF
        #------------------------------------------------------------------------------------


        # merge the dataframes based on 'ZEICHNUNG' and 'Drawing Revision' columns
        merged_df_PDF = pd.merge(bom_list, df_list_of_PDF, left_on=['ZEICHNUNG', 'Drawing Revision'], right_on=['identifier', 'version'], how='left')
        # create a new DataFrame of missing PDFs
        df_missing_PDFs = merged_df_PDF[merged_df_PDF['identifier'].isna()][['ZEICHNUNG', 'Drawing Revision']]
        # create a new DataFrame of non-missing PDFs
        df_non_missing_PDFs = merged_df_PDF[~merged_df_PDF['identifier'].isna()][['ZEICHNUNG', 'Drawing Revision', 'path']]

        #-----------------------------------------------------------
        bom_name = bom_list.loc[0, 'ARTIKEL']
        # bom_name = hal
        #-----------------------------------------------------------
        # print(df_missing_PDFs)
        output_path = os.path.join(folder_path, 'DRW to print')
        if not os.path.exists(output_path):
            os.makedirs(output_path)

        if not df_missing_PDFs.empty:
            missing_PDF_filepath = os.path.join(output_path, bom_name + "-drawings_missing.txt")
            with open(missing_PDF_filepath, 'w') as f:
                    f.write(df_missing_PDFs.to_string(index=False))
            # chybajuce_vykres_path = os.path.abspath(folder_path + "-Chybajuce PDF.txt") 

        #-----------------------------------------------------------------------------------------
        
        output_path_PDF = os.path.join(output_path, bom_name + "-drawings_merged.pdf")
                      
        def print_PDFs():
            # create a PDF writer object
            pdf_writer = PyPDF2.PdfWriter()

            # loop through the PDFs in df_non_missing_PDFs and add them to the writer object
            for index, row in df_non_missing_PDFs.iterrows():
                pdf_path = row['path']
                with open(pdf_path, 'rb') as pdf_file:
                    pdf_reader = PyPDF2.PdfReader(pdf_file)
                    for page_num in range(len(pdf_reader.pages)):
                        page = pdf_reader.pages[page_num]
                        pdf_writer.add_page(page)

            # write the combined PDF to disk
            with open(output_path_PDF, 'wb') as output_file:
                pdf_writer.write(output_file)


        print_PDFs()
          

        #----------------------------------------------------------------------------------
        # KONTROLA AKTUALNOSTI STEP
        #------------------------------------------------------------------------------------
        filtered_bom_list_0 = bom_list[~(((bom_list['ZEICHNUNG'] == "") | pd.isna(bom_list['ZEICHNUNG'])) & ((bom_list['ARTIKEL'] == "") | pd.isna(bom_list['ARTIKEL'])))]
        filtered_bom_list =  filtered_bom_list_0[filtered_bom_list_0['Art'] != "BG"]
 
        if not filtered_bom_list.empty:
            # Merge the dataframes based on 'ARTIKEL' and 'Drawing Revision' columns
            merged_df_STEP = pd.merge(filtered_bom_list, df_list_of_STEP, left_on=['ARTIKEL', 'Drawing Revision'], right_on=['identifier', 'version'], how='left')

            # Create a new DataFrame of missing PDFs
            df_missing_STEPs = merged_df_STEP[merged_df_STEP['identifier'].isna()][['ARTIKEL', 'ZEICHNUNG', 'Drawing Revision']]

            # Append missing data to the storage DataFrame
            storage_df = pd.concat([storage_df, df_missing_STEPs])


    if not storage_df.empty:
        storage_df = storage_df.reset_index(drop=True).drop_duplicates(subset=['ARTIKEL', 'ZEICHNUNG', 'Drawing Revision'], ignore_index=True)
        missing_STEP_filepath = os.path.join(folder_path, "STEPs missing.csv")
        storage_df.to_csv(missing_STEP_filepath, index=False)
        # with open(missing_STEP_filepath, 'w') as f:
        #     f.write(storage_df.to_string(index=False))

    
