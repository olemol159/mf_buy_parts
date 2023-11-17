import os
import pandas as pd

#------------------------------------------------------------------------------------------------------
def get_dataframes(path_PDF, path_STEP):

    dir_list_PDF = os.listdir(path_PDF) # číta súbor

    data_PDF = []
    for file_PDF in dir_list_PDF:
        filename_PDF, extension_PDF = os.path.splitext(file_PDF)
        if "-r" in filename_PDF:
            parts_pdf = filename_PDF.split("-")
            identifier_pdf = "".join(parts_pdf[:len(parts_pdf) - 1])
            version_pdf = parts_pdf[-1][-2:]
        else:
            identifier_pdf = filename_PDF
            version_pdf = "XX"
        path_pdf = os.path.join(path_PDF, file_PDF) # add path to file
        data_PDF.append({'identifier': identifier_pdf, 'version': version_pdf, 'path': path_pdf})

    for i in range(len(data_PDF)):
        data_PDF[i]['identifier'] = data_PDF[i]['identifier'].strip()
        data_PDF[i]['version'] = data_PDF[i]['version'].strip()

    df_list_of_PDF = pd.DataFrame(data_PDF)

    # with open("df_list_of_PDF.txt", "w", encoding="utf-8") as f:
    #     f.write(df_list_of_PDF.to_string(index=False))
    # print(df_list_of_PDF)

#------------------------------------------------------------------------------------------------------

    dir_list_STEP = os.listdir(path_STEP) # číta súbor

    data_STEP = []
    for file_STEP in dir_list_STEP:
        filename_STEP, extension_STEP = os.path.splitext(file_STEP)
        if "-r" in filename_STEP:
            parts_STEP = filename_STEP.split("-")
            identifier_STEP = filename_STEP[:10]
            version_STEP = parts_STEP[-1][-2:]
        else:
            identifier_STEP = filename_STEP
            version_STEP = "XX"
        data_STEP.append({'identifier': identifier_STEP, 'version': version_STEP})


    df_list_of_STEP = pd.DataFrame(data_STEP)


    # print(df_list_of_STEP)
    # with open("df_list_of_STEP.txt", "w", encoding="utf-8") as f:
    #     f.write(df_list_of_STEP.to_string(index=False))


    new_var = df_list_of_PDF, df_list_of_STEP
    return new_var

