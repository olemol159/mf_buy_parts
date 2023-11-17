import pickle
from fpdf import FPDF 

import os


def pdf_bom_creation_tool(folder_path):

    help_assy_list= os.listdir(os.path.join(folder_path, 'temp'))

    for hal in help_assy_list:

        file_path = os.path.join(folder_path, 'temp', hal)

        with open(file_path, 'rb') as file: # nahrá iterovanú rozpisku
            bom_list = pickle.load(file)    
        # os.remove('df_final.pkl')   # po vytvorení rozpisky odstráni pomocný súbor

        selected_columns = [
        "EB", "BG_ARTIKELNR", "Art", 'POS', "ARTIKEL", "ZEICHNUNG", "OVL Numbers", "DRW REV", "MENGE", "ME", 'BEZEICH', 'MEMO_TECH', 'DRW FOR' 
        ]

        bom_final = bom_list[selected_columns]

            # with open("FINAL ROZPISKA.txt", "w", encoding="utf-8") as f:
        #         f.write(df_final.to_string(index=False))

        # with open("df2.txt", "w", encoding="utf-8") as f:
        #     f.write(df2.to_string(index=False))

        # with open("FINAL ROZPISKA.txt", "w", encoding="utf-8") as f:
        #         f.write(df_final.to_string(index=False))
        #---------------------------------------------------------------
        #  PDF tvorba 

        pdf = FPDF(format='A3', orientation='L')
        pdf.add_page()

        class PDF(FPDF):
            def header(self):
                # Add the header image here if needed
                pass

            def footer(self):
                # Add page number and footer text here if needed
                self.set_y(-15)
                self.set_font('Arial', 'I', 8)
                self.cell(0, 10, f'Page {self.page_no()}/{{nb}}', 0, 0, 'C')

        # Initialize the PDF object
        pdf = PDF('L', 'mm', 'A3')
        pdf.add_page()

        # Set the font and font size for table content
        pdf.set_font('Arial', 'B', 8.5)

        # Set up the table header
        data_cell_width_wide = 92.5
        data_cell_width_short = 10
        data_cell_width_2 = 12.5
        data_cell_width_1 = 22.5
        data_cell_width_3 = 17
        data_cell_width_4 = 47.5
        data_cell_width_5 = 32.5
        data_cell_width_6 = 7.5
        data_cell_height = 5


        headers = bom_final.columns.tolist()
        for header in headers:
            if header in ["Art", "MENGE", "ME", 'POS']:
                cell_width = data_cell_width_short
                alignment = 'C'
            elif header in ["BG_ARTIKELNR", "ZEICHNUNG"]:
                cell_width = data_cell_width_1
                alignment = 'C'
            elif header in ["OVL Numbers"]:
                cell_width = data_cell_width_5
                alignment = 'C'
            elif header in ["ARTIKEL"]:
                cell_width = data_cell_width_4
                alignment = 'R'
            elif header in ["DRW REV"]:
                cell_width = data_cell_width_3
                alignment = 'C'
            elif header in ["EB"]:
                cell_width = data_cell_width_6
                alignment = 'C'
            elif header in ['DRW FOR']:
                cell_width = data_cell_width_2
                alignment = 'C'
            else:
                cell_width = data_cell_width_wide
                alignment = "L"

            cell_text = str(header)
            pdf.cell(cell_width, 8, cell_text, border=0, ln=0, align=alignment)    
        pdf.ln()

        # Set the font and font size for table content
        pdf.set_font('Arial', '', 9)

        bg_artikelnr_values = bom_final['BG_ARTIKELNR'].unique()
        num_values = len(bg_artikelnr_values)
        color_map = {}
        #color_step = 220 // num_values
        colors = [(255, 255, 255), 
                  (100, 149, 237), 
                  (204, 229, 255), 
                  (205, 255, 140), 
                  (255, 175, 175), 
                  (72, 209, 204), 
                  (192, 192, 192), 
                  (238, 130, 238), 
                  (152, 251, 152), 
                  (255, 204, 255),
                  (255, 255, 255)    # white set as deault if not founded value for 'EB'
                ]
        
        color_map = {
                    "0": colors[0],
                    "1": colors[1],
                    "2": colors[2],
                    "3": colors[3],
                    "4": colors[4],
                    "5": colors[5]
                    }
        # for i, value in enumerate(bg_artikelnr_values):
        #     color_map[value] = colors[i % len(colors)]

        #headers = ["BG_ARTIKELNR", "Art", "ZEICH_POSN", "ARTIKEL", "ZEICHNUNG", "OVL Numbers", "Drawing Revision", "MENGE", "ME","BEZEICH", "MEMO_TECH", "Drawing size"]

        # Add the dataframe to the PDF
        for index, row in bom_final.iterrows():
            if index == 1:
                #pdf.cell(0, 0, '', border=1, ln=1, fill=False)  # draw a line after the first row
                #pdf.rect(pdf.l_margin, pdf.y, pdf.w, 0.1)  # add line
                pdf.line(10, pdf.y, 400, pdf.y)
                pdf.ln()  # add blank line after the first row
                
            for header in headers:
                if header == 'EB' or header == 'BG_ARTIKELNR':
                    cell_value = row['EB']  # Assuming 'EB' is the column name
                    fill_color = color_map.get(cell_value, colors[-1])  # Default to white if no mapping is found
                    pdf.set_fill_color(*fill_color)
                else:
                    pdf.set_fill_color(255, 255, 255)

                if header in ["Art", "MENGE", "ME", 'POS']:
                    cell_width = data_cell_width_short
                    alignment = 'C'
                elif header in ["BG_ARTIKELNR", "ZEICHNUNG"]:
                    cell_width = data_cell_width_1
                    alignment = 'C'
                elif header in ["OVL Numbers"]:
                    cell_width = data_cell_width_5
                    alignment = 'C'
                elif header in ["ARTIKEL"]:
                    cell_width = data_cell_width_4
                    alignment = 'R'
                elif header in ["DRW REV"]:
                    cell_width = data_cell_width_3
                    alignment = 'C'
                elif header in ["EB"]:
                    cell_width = data_cell_width_6
                    alignment = 'C'
                elif header in ['DRW FOR']:
                    cell_width = data_cell_width_2
                    alignment = 'C'
                else:
                    cell_width = data_cell_width_wide
                    alignment = "L"


                cell_text = str(row[header])
                if pdf.get_string_width(cell_text) > cell_width:
                    lines = pdf.multi_cell(cell_width, 8, cell_text, border=0, align=alignment, fill=True)
                    pdf.ln(8 * (len(lines) - 1))  # move cursor to next line
                else:
                    pdf.cell(cell_width, 8, cell_text, border=0, ln=0, align=alignment, fill=True)
            pdf.ln()

        # Save the PDF file
        bom_name = bom_final.loc[0, 'ARTIKEL']
        if not os.path.exists(os.path.join(folder_path, 'BOMs lists')):
            os.makedirs(os.path.join(folder_path, 'BOMs lists'))
        bom_file_path = os.path.join(folder_path, 'BOMs lists', bom_name + '.pdf')
        pdf.output(bom_file_path, 'F')
 




