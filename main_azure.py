import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter.ttk import *
from tkinter import filedialog
from tkinter import messagebox
import os

import buy_parts
import sorting
import ovl_assign
import normal_bom_creation
import solo_group
import rename
import topicality_checking
import pdf_bom
import remove_temp_files

buy_parts_path = 'D:\\NaucSePython\\data\\MF_BuyParts.xlsx'
# buy_parts_path = "\\\\serverfs\Vykresy\ZAHRANIČNÍ ZÁKAZNÍCI\MF-Hamburg Maschinen\VÝKRESY\Výroba\VZOR_MF_BuyParts.xlsx" # priamá cesta k súboru s MF BuyParts .. moôže byť súbor aj inak pomenovaný
erzeugnis_json_path = "D:\\NaucSePython\\data\\VZOR_Erzeugnis_Kuhl.json" # umiestnenie súboru
# erzeugnis_json_path = "\\\\serverfs\Vykresy\ZAHRANIČNÍ ZÁKAZNÍCI\MF-Hamburg Maschinen\VÝKRESY\Výroba\VZOR_Erzeugnis_Kuhl.json" # umiestnenie súboru
path_PDF = "D:\\NaucSePython\\data\\PDF" # umiestnenie súboru
# path_PDF = "\\\\serverfs\Vykresy\ZAHRANIČNÍ ZÁKAZNÍCI\MF-Hamburg Maschinen\VÝKRESY\Výroba\PDF" 
path_STEP = "D:\\NaucSePython\\data\\STEP" # umiestnenie súboru
# path_STEP = "\\\\serverfs\Vykresy\ZAHRANIČNÍ ZÁKAZNÍCI\MF-Hamburg Maschinen\VÝKRESY\Výroba\STEP" # umiestnenie súboru

root=tk.Tk()
# screen_width = root.winfo_screenwidth()
screen_width = 2560
# screen_height = root.winfo_screenheight()
screen_height = 1650
x_start_position = 5
y_start_position = 5
root.geometry(f"{int(700)}x{int(screen_height/2)}+{x_start_position}+{y_start_position}" )



# if platform.system() == "Windows":
#     #root.state("zoomed")
# else:
#     root.state("normal")





root.title("Azure GUI")

style = ttk.Style(root)
root.tk.call('source','azure dark 3.tcl')
style.theme_use('azure')

options = ['', 'OptionMenu', 'Value 1', 'Value 2']
a = tk.IntVar()
b = tk.IntVar()
b.set(1)
c = tk.IntVar()
d = tk.IntVar()
d.set(1)
e = tk.StringVar()
e.set(options[1])
f = tk.IntVar()
g = tk.IntVar()
g.set(75)
h = tk.IntVar()

frame1 = ttk.LabelFrame(root, text='File path', width=600, height=140)
frame1.place(x=40, y=100)

frame2 = ttk.LabelFrame(root, text='Folder path', width=600, height=140)
frame2.place(x=40, y=272)

frame3 = ttk.LabelFrame(root, text='Option', width=600, height=200)
frame3.place(x=40, y=435)

# frame4 = ttk.LabelFrame(root, text='Menu', width=700, height=400)
# frame4.place(x=int(screen_width-800), y=40)

# status_bar = ttk.LabelFrame(root, text='Option', width=420, height=200)
# status_bar.place(x=40, y=435)




label_entry = ttk.Label(root, text="Project number:", font=("TkDefaultFont", 8, "bold"))
label_entry.place(x=40, y=20)
entry = ttk.Entry(root, width=20)#, text="Entry")
entry.place(x=40, y=40)
#entry.insert(0, 'Project number')

label_combo = ttk.Label(root, text="Width variant:", font=("TkDefaultFont", 8, "bold"))
label_combo.place(x=490, y=20)
combo = ttk.Combobox(root, width=20, state='readonly', value=['620', '680', '820', '870', '1050', '1070', '1200', '1300', '1400', '1500', '1600', '1700', '1800', '2000', '2300'])
combo.current(0)
combo.place(x=490, y=40)

#------------------frame1-------------------------------
def get_file_path():
    global file_path
    file_path = filedialog.askopenfilename(initialdir = "C:",
                                           title = "Select a File",
                                           filetypes = (("Excel files",
                                                         "*.xlsm*"),
                                                        ("Text files",
                                                         "*.txt*"),
                                                        ("All files",
                                                         "*.*")))
    if file_path:
        file_path_label_2.configure(text=file_path)
    else:
        file_path_label_2.configure(text="-no file selected-")
        file_path = "-no file selected-"
    return file_path

file_path = '-no file selected-'
file_path_button = ttk.Button(
    frame1,
    width=20,
    text='Select a file',
    style='Accentbutton',
    command=get_file_path
    )
file_path_button.place(x=20, y=20)
file_path_label = ttk.Label(frame1, text="File path:", font=("TkDefaultFont", 10, "bold"))
file_path_label.place(x=20, y=70)
file_path_label_2 = ttk.Label(frame1, text=file_path)
file_path_label_2.place(x=20, y=90)








#-------------------------------------------------------


#------------------frame2-------------------------------
def get_folder_path():
    global folder_path
    folder_path = filedialog.askdirectory(initialdir="C:")
                                           
    if folder_path:
        folder_path_label_2.configure(text=folder_path)
    else:
        folder_path_label_2.configure(text="-no folder selected-")
        folder_path = "-no folder selected-"
    return folder_path

folder_path = '-no folder selected-'
folder_path_button = ttk.Button(
    frame2,
    width=20,
    text='Select a folder',
    style='Accentbutton',
    command=get_folder_path
    )
folder_path_button.place(x=20, y=20)
folder_path_label = ttk.Label(frame2, text="Folder path:", font=("TkDefaultFont", 10, "bold"))
folder_path_label.place(x=20, y=70)
folder_path_label_2 = ttk.Label(frame2, text=folder_path)
folder_path_label_2.place(x=20, y=90)

#-------------------------------------------------------




#------------------frame3-------------------------------
xf3 = 30
disabled = ttk.Radiobutton(frame3, text='Normal', variable=d, value=1)
disabled.place(x=xf3, y=20)
bwe = ttk.Radiobutton(frame3, text='BWE', variable=d, value=2)
bwe.place(x=xf3, y=60)
nbv = ttk.Radiobutton(frame3, text='NBV', variable=d, value=3)
nbv.place(x=xf3, y=100)
others = ttk.Radiobutton(frame3, text='Others', variable=d, value=4)
others.place(x=xf3, y=140)
#-------------------------------------------------------
def next_button():
    project_number = entry.get().strip()
    width_variant = combo.get()
    bom_type = d.get()

    # print(project_number, width_variant, file_path, folder_path, bom_type)
    if not os.path.exists(buy_parts_path):
        root = tk.Tk()
        root.withdraw()  # Hide the main window
        messagebox.showerror("Error", f"The specified path does not exist.\n{buy_parts_path} \n\n Please insert a file into folder.")
    elif not os.path.exists(erzeugnis_json_path):
        root = tk.Tk()
        root.withdraw()  # Hide the main window
        messagebox.showerror("Error", f"The specified path does not exist.\n{erzeugnis_json_path} \n\n Please insert a file into folder.")
    elif (project_number == '' or project_number is None) and file_path == '-no file selected-' and folder_path == '-no folder selected-':
        messagebox.showerror('Error', 'Following data are missing:\n\n- Project number\n- File path\n- Folder path')
    elif (project_number == '' or project_number is None) and file_path == '-no file selected-':
        messagebox.showerror('Error', 'Following data are missing:\n\n- Project number\n- File path')
    elif (project_number == '' or project_number is None) and folder_path == '-no folder selected-':
        messagebox.showerror('Error', 'Following data are missing:\n\n- Project number\n- Folder path')
    elif (project_number == '' or project_number is None):
        messagebox.showerror('Error', 'Following data are missing:\n\n- Project number')
    elif file_path == '-no file selected-' and folder_path == '-no folder selected-':
        messagebox.showerror('Error', 'Following data are missing:\n\n- File path\n- Folder path')
    elif file_path == '-no file selected-':
        messagebox.showerror('Error', 'Following data are missing:\n\n- File path')
    elif folder_path == '-no folder selected-':
        messagebox.showerror('Error', 'Following data are missing:\n\n- Folder path')
    else:
        sorting.get_df_rozpiska(file_path, folder_path)       # nahranie dát rozpisky a filtrovanie stĺpcov
        task('sorting done',12.5)
        buy_parts.get_buy_parts(folder_path, buy_parts_path)      # príprava a nahratie dát BuyParts
        task('Buy Parts input done',25)
        ovl_assign.get_assign(folder_path)       # priradenie OVL
        task('OVL assign done',37.5)
        if bom_type == 1:
            normal_bom_creation.bom_creation_tool(folder_path)
            task('SUB GROUPS creation done',50)
        else:
            solo_group.bom_creation_tool(folder_path)
            task('GROUP creation done',50)        
        topicality_checking.checking_tool(folder_path, path_PDF, path_STEP)
        task('DRAWINGS checking done', 62.5)
        rename.bom_renaiming(folder_path, erzeugnis_json_path, width_variant, project_number)
        task('rename columns done', 75)
        pdf_bom.pdf_bom_creation_tool(folder_path)
        task('BOMs creation done', 87.5)
        remove_temp_files.remove_tool(folder_path)
        task('TASK COMPLETED', 100)


next = ttk.Button(
    root,
    width=35,
    compound="center",
    text='Create BOMs with Drawings to print',
    style='Accentbutton',
    command=next_button
    )
next.place(x=405, y=650)

#------------------status bar--------------------------
def task(current_operation, task_weight):
    bar['value'] = task_weight
    percent.set(str(task_weight)+'%')
    operation.set(str(current_operation))
    root.update_idletasks()

percent = StringVar()
operation = StringVar()

status_bar_label = ttk.Label(root, text='Status bar :')
status_bar_label.place(x=40, y=710)

percent_label = Label(root, textvariable=operation)
percent_label.place(x=40, y=735)

operation_label = Label(root, textvariable=percent)
operation_label.place(x=580, y=735)

style = ttk.Style()
# style.configure("TProgressbar", thickness=20)
bar = Progressbar(root, orient=HORIZONTAL, length=580)#, mode='indeterminate', style="TProgressbar")
bar.place(x=45, y=750)



#-------------------------------------------------------

# sep1 = ttk.Separator()
# sep1.place(x=20, y=int(screen_height-400), width=480)


#-------------------------------------------------------

# ntw = 500
# nth = 200 
# notebook = ttk.Notebook(root)
# notebookTab1 = ttk.Frame(notebook, width=ntw, height=nth)
# notebook.add(notebookTab1, text='Chybajuce PDF')
# notebookTab2 = ttk.Frame(notebook, width=ntw, height=nth)
# notebook.add(notebookTab2, text='Chybajúce STEP')
# notebookTab3 = ttk.Frame(notebook, width=ntw, height=nth)
# notebook.add(notebookTab3, text='Tab 3')
# notebook.place(x=int(screen_width-1.25*ntw), y=int(screen_height/4-330))




# # Create the frame to hold the results
# results_frame = ttk.Frame(root)
# results_frame.pack(x=int(screen_width-1.5*ntw), y=int(20))

# # Create the scrollbar for the results frame
# scrollbar = ttk.Scrollbar(results_frame)
# scrollbar.pack(side=RIGHT, fill=Y)

# # Create the widget to display the results (e.g., Treeview or Text)
# results_widget = ttk.Treeview(results_frame, yscrollcommand=scrollbar.set)
# results_widget.pack()

# # Configure the scrollbar to scroll the results widget
# scrollbar.config(command=results_widget.yview)




# canvas = tk.Canvas(root)
# canvas.place(x=int(screen_width-500), y=int(20))
# scrollbar = tk.Scrollbar(root, orient='vertical', command=canvas.yview)
# scrollable_frame = tk.Frame(canvas)




# frame = ttk.Frame(root, width= 80, height = 80)
# frame.place(x=int(screen_width-1.5*ntw), y=int(20), relwidth=0.4, relheight=0.8)

# # create a ttk Scrollbar and pack it inside the frame
# scrollbar = ttk.Scrollbar(frame)
# scrollbar.pack(side='right', fill='y')

# # add some widgets to the frame
# for i in range(10):
#     ttk.Label(frame, text=f"Label {i}").pack()




# treeview = ttk.Treeview(treeFrame, selectmode="extended", yscrollcommand=treeScroll.set, columns=(1, 2), height=12)
# treeview.pack()
# treeScroll.config(command=treeview.yview)

root.mainloop()