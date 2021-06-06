### data correction with python
import os
import pandas as pd
import mysql.connector
import xlrd
import datetime
import pymysql
import tkinter as tk
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import re


def isNaN(num):
    return num != num


def ugrad_department(row):
    if isNaN(row['UGrad Department']):
        return ''
    if (((row['UGrad Department'].find('COMPUTER') >= 0) or (row['UGrad Department'].find('BİLGİSAYAR') >= 0))
            and (row['UGrad Department'].find('ÖĞRET') < 0)
            and (row['UGrad Department'].find('TEACH') < 0)
            and (row['UGrad Department'].find('EDUCATİON') < 0)):
        return 'CMPE OR SIMILAR'
    return 'OTHER'


def ugrad_second_department(row):
    if isNaN(row['UGrad Second Dept']):
        return ''
    if (((row['UGrad Second Dept'].find('COMPUTER') >= 0) or (row['UGrad Second Dept'].find('BİLGİSAYAR') >= 0))
            and (row['UGrad Second Dept'].find('ÖĞRET') < 0)
            and (row['UGrad Second Dept'].find('TEACH') < 0)
            and (row['UGrad Second Dept'].find('EDUCATİON') < 0)):
        return 'CMPE OR SIMILAR'
    return 'OTHER'


def grad_program(row):
    if isNaN(row['Grad Program']):
        return ''
    if (((row['Grad Program'].find('COMPUTER') >= 0) or (row['Grad Program'].find('BİLGİSAYAR') >= 0))
            and (row['Grad Program'].find('ÖĞRET') < 0)
            and (row['Grad Program'].find('TEACH') < 0)
            and (row['Grad Program'].find('EDUCATİON') < 0)):
        return 'CMPE OR SIMILAR'
    return 'OTHER'


# replace turkish characters
def replace_turkish_characters(str):
    if isNaN(str):
        return ''
    str = str.replace("Ğ", "G")
    str = str.replace("Ü", "U")
    str = str.replace("Ç", "C")
    str = str.replace("İ", "I")
    str = str.replace("Ş", "S")
    str = str.replace("Ö", "O")
    str = str.replace("  ", " ")
    return str


# get grade (first part of CGPA)
def get_grade(row):
    if isNaN(row['UGrad CGPA']):
        return ''
    if (row['UGrad CGPA'].find('/') < 0):
        return ''
    else:
        cgpa = row['UGrad CGPA']
        grade = round(float(cgpa[:cgpa.find('/') - 1].replace(',', '.')), 2)
        return grade


# get grade scale (second part of CGPA)
def get_grade_scale(row):
    if isNaN(row['UGrad CGPA']):
        return ''
    if (row['UGrad CGPA'].find('/') < 0):
        return ''
    else:
        cgpa = row['UGrad CGPA']
        scale = len(cgpa) - cgpa.find('/') - 2
        grade = round(float(cgpa[-scale:].replace(',', '.')), 2)
        return grade


def get_files():
    global file_path
    file_path = tk.filedialog.askopenfilenames(filetypes=[("Excel files", "*.xls*")])
    top.destroy()


def skip():
    top.destroy()


def restart_app():
    print("deneme")
    top.destroy
    python = sys.executable
    os.execl(python, python, *sys.argv)

def keyword_entry():
    global enter
    enter = 1
    top.destroy()


def save_and_print():
    ok = 1
    global li
    global uni_name

    k1 = K1.get().upper()
    k2 = K2.get().upper()
    k3 = K3.get().upper()
    k4 = K4.get().upper()
    k5 = K5.get().upper()

    uni_name = Uni_box.get().upper()
    uni_cluster = variable.get().upper()

    if uni_cluster == 'OTHER' or uni_cluster == 'Other' or uni_cluster == '':
        uni_cluster = 'XX'

    if isNaN(uni_name) or uni_name == '' or uni_name == ' ' or len(uni_name) < 15:
        messagebox.showinfo("Error", "At least 15-character 'University Name' is mandatory.")
        ok = 0  # cannot be saved

    if isNaN(k1) or k1 == '' or k1 == ' ' or len(k1) < 3:
        messagebox.showinfo("Error", "At least 3-character 'Keyword 1' is mandatory.")
        ok = 0
    else:
        li.append(k1)

    if isNaN(k2) or k2 == '' or k2 == ' ':
        pass
    elif 0 < len(k2) < 3:
        messagebox.showinfo("Error", "'Keyword 2' should be empty or have at least 3-characters.")
        ok = 0
    else:
        if k2 not in li:
            li.append(k2)
        else:
            messagebox.showinfo("Error", "'Keyword 2' is entered before. It will not be added to keyword list.")

    if isNaN(k3) or k3 == '' or k3 == ' ':
        pass
    elif 0 < len(k3) < 3:
        messagebox.showinfo("Error", "'Keyword 3' should be empty or have at least 3-characters.")
        ok = 0
    else:
        if k3 not in li:
            li.append(k3)
        else:
            messagebox.showinfo("Error", "'Keyword 3' is entered before. It will not be added to keyword list.")

    if isNaN(k4) or k4 == '' or k4 == ' ':
        pass
    elif 0 < len(k4) < 3:
        messagebox.showinfo("Error", "'Keyword 4' should be empty or have at least 3-characters.")
        ok = 0
    else:
        if k4 not in li:
            li.append(k4)
        else:
            messagebox.showinfo("Error", "'Keyword 4' is entered before. It will not be added to keyword list.")

    if isNaN(k5) or k5 == '' or k5 == ' ':
        pass
    elif 0 < len(k5) < 3:
        messagebox.showinfo("Error", "'Keyword 5' should be empty or have at least 3-characters.")
        ok = 0
    else:
        if k5 not in li:
            li.append(k5)
        else:
            messagebox.showinfo("Error", "'Keyword 5' is entered before. It will not be added to keyword list.")

    if ok == 1:
        save_uni_keywords_to_db(li, uni_name, uni_cluster)
        messagebox.showinfo("Successful", uni_name + " and keywords: " + str(li) + " saved successfully.")
        top.destroy()


def save_uni_keywords_to_db(kw_list, uni, u_cluster):
    global connection

    cursor = connection.cursor()
    add_uni = ("INSERT INTO university "
               "(name, cluster) "
               "VALUES (%s, %s)")

    uni_data = (uni, u_cluster)

    # Insert new university
    cursor.execute(add_uni, uni_data)

    uni_id = cursor.lastrowid

    add_keyword = ("INSERT INTO keyword "
                   "(keyword, university_id) "
                   "VALUES (%s, %s)")

    print("last_uni_id", uni_id)
    print("type_uni_id", type(uni_id))

    for i in kw_list:
        keyword_data = (i, uni_id)
        # insert keyword
        cursor.execute(add_keyword, keyword_data)

    connection.commit()


def save_grade_clusters():
    ok = 1
    grade_list = []
    global uni_name

    global a_star_max_grade
    grade_a_star_max = a_star_max_grade.get()
    grade_list.append(grade_a_star_max)
    global a_star_min_grade
    grade_a_star_min = a_star_min_grade.get()
    grade_list.append(grade_a_star_min)
    global a_max_grade
    grade_a_max = a_max_grade.get()
    grade_list.append(grade_a_max)
    global a_min_grade
    grade_a_min = a_min_grade.get()
    grade_list.append(grade_a_min)
    global b_max_grade
    grade_b_max = b_max_grade.get()
    grade_list.append(grade_b_max)
    global b_min_grade
    grade_b_min = b_min_grade.get()
    grade_list.append(grade_b_min)
    global c_max_grade
    grade_c_max = c_max_grade.get()
    grade_list.append(grade_c_max)
    global c_min_grade
    grade_c_min = c_min_grade.get()
    grade_list.append(grade_c_min)
    global d_max_grade
    grade_d_max = d_max_grade.get()
    grade_list.append(grade_d_max)
    global d_min_grade
    grade_d_min = d_min_grade.get()
    grade_list.append(grade_d_min)

    for Grade in grade_list:
        if Grade:
            print(Grade)
        else:
            messagebox.showinfo("Error", "Input all max and min grades")
            ok = 0
    if ok == 1:
        save_grade_clusters_to_db(grade_list)
        messagebox.showinfo("Successful", "Grade Clusters saved successfully.")
        top.destroy()


def save_grade_clusters_to_db(grade_lists):
    count = 1
    for i in range(len(grade_lists)):
        if i % 2 == 0:
            print(i)
            global connection
            cursor = connection.cursor()
            update_grade = ("UPDATE GRADE_CLUSTER SET "
                            "MAX_GPA=%s, MIN_GPA=%s WHERE ID=%s")

            grade_data = (grade_lists[i], grade_lists[i+1], count)

            # Update grade clusters
            cursor.execute(update_grade, grade_data)
            connection.commit()
            count = count + 1


def save_requirements():
    ok = 1
    requirements_list = []

    global ales_min_grade
    grade_ales_min = ales_min_grade.get()
    requirements_list.append(grade_ales_min)
    global gre_min_grade
    grade_gre_min = gre_min_grade.get()
    requirements_list.append(grade_gre_min)
    global yds_min_grade
    grade_yds_min = yds_min_grade.get()
    requirements_list.append(grade_yds_min)
    global ielts_overall_min_grade
    grade_ielts_overall_min = ielts_overall_min_grade.get()
    requirements_list.append(grade_ielts_overall_min)
    global ielts_write_min_grade
    grade_ielts_write_min = ielts_write_min_grade.get()
    requirements_list.append(grade_ielts_write_min)
    global toefl_overall_min_grade
    grade_toefl_overall_min = toefl_overall_min_grade.get()
    requirements_list.append(grade_toefl_overall_min)
    global toefl_write_min_grade
    grade_toefl_write_min = toefl_write_min_grade.get()
    requirements_list.append(grade_toefl_write_min)

    for req in requirements_list:
        if req:
            print(req)
        else:
            messagebox.showinfo("Error", "Input all fields")
            ok = 0
    if ok == 1:
        save_requirements_to_db(requirements_list)
        messagebox.showinfo("Successful", "Requirements saved successfully.")
        top.destroy()


def save_requirements_to_db(requirements_list):
    print(requirements_list)
    global connection
    cursor = connection.cursor()
    update_grade = ("UPDATE REQUIREMENTS SET "
                    "ALES_MIN=%s, GRE_MIN=%s, YDS_MIN=%s, IELTS_OVERALL_MIN=%s,"
                    "IELTS_WRITE_MIN=%s, TOEFL_OVERALL_MIN=%s, TOEFL_WRITE_MIN=%s WHERE ID=1")
    grade_data = tuple(requirements_list)
    cursor.execute(update_grade, grade_data)
    connection.commit()


def requirements():
    skip()
    global requirements_df
    top = Tk()
    top.title("Requirements")
    top.geometry("300x400")

    ales_min = Label(top, text="ALES Min")
    ales_min.pack()
    ales_min.place(x=30, y=30)

    gre_min = Label(top, text="GRE Min")
    gre_min.pack()
    gre_min.place(x=30, y=60)

    yds_min = Label(top, text="YDS Min")
    yds_min.pack()
    yds_min.place(x=30, y=90)

    ielts_overall_min = Label(top, text="IELTS Overall Min")
    ielts_overall_min.pack()
    ielts_overall_min.place(x=30, y=120)

    ielts_write_min = Label(top, text="IELTS Write Min")
    ielts_write_min.pack()
    ielts_write_min.place(x=30, y=150)

    toefl_overall_min = Label(top, text="TOEFL Overall Min")
    toefl_overall_min.pack()
    toefl_overall_min.place(x=30, y=180)

    toefl_write_min = Label(top, text="TOEFL Write Min")
    toefl_write_min.pack()
    toefl_write_min.place(x=30, y=210)

    global ales_min_grade
    ales_min_grade = StringVar()
    ales_min_grade = Entry(top, textvariable=ales_min_grade)
    ales_min_grade.insert(INSERT, requirements_df.iloc[0]['ALES_MIN'])
    ales_min_grade.pack()
    ales_min_grade.place(x=150, y=30, width=50)

    global gre_min_grade
    gre_min_grade = StringVar()
    gre_min_grade = Entry(top, textvariable=gre_min_grade)
    gre_min_grade.insert(INSERT, requirements_df.iloc[0]['GRE_MIN'])
    gre_min_grade.pack()
    gre_min_grade.place(x=150, y=60, width=50)

    global yds_min_grade
    yds_min_grade = StringVar()
    yds_min_grade = Entry(top, textvariable=gre_min_grade)
    yds_min_grade.insert(INSERT, requirements_df.iloc[0]['YDS_MIN'])
    yds_min_grade.pack()
    yds_min_grade.place(x=150, y=90, width=50)

    global ielts_overall_min_grade
    ielts_overall_min_grade = StringVar()
    ielts_overall_min_grade = Entry(top, textvariable=ielts_overall_min_grade)
    ielts_overall_min_grade.insert(INSERT, requirements_df.iloc[0]['IELTS_OVERALL_MIN'])
    ielts_overall_min_grade.pack()
    ielts_overall_min_grade.place(x=150, y=120, width=50)

    global ielts_write_min_grade
    ielts_write_min_grade = StringVar()
    ielts_write_min_grade = Entry(top, textvariable=ielts_write_min_grade)
    ielts_write_min_grade.insert(INSERT, requirements_df.iloc[0]['IELTS_WRITE_MIN'])
    ielts_write_min_grade.pack()
    ielts_write_min_grade.place(x=150, y=150, width=50)

    global toefl_overall_min_grade
    toefl_overall_min_grade = StringVar()
    toefl_overall_min_grade = Entry(top, textvariable=toefl_overall_min_grade)
    toefl_overall_min_grade.insert(INSERT, requirements_df.iloc[0]['TOEFL_OVERALL_MIN'])
    toefl_overall_min_grade.pack()
    toefl_overall_min_grade.place(x=150, y=180, width=50)

    global toefl_write_min_grade
    toefl_write_min_grade = StringVar()
    toefl_write_min_grade = Entry(top, textvariable=toefl_write_min_grade)
    toefl_write_min_grade.insert(INSERT, requirements_df.iloc[0]['TOEFL_WRITE_MIN'])
    toefl_write_min_grade.pack()
    toefl_write_min_grade.place(x=150, y=210, width=50)

    B1 = Button(top, text="Cancel", command=restart_app, fg='White', bg='dark green', height=1, width=10)
    B1.pack()
    B1.place(x=30, y=250)

    B2 = Button(top, text="Save", command=save_requirements, fg='White', bg='dark green', height=1, width=10)
    B2.pack()
    B2.place(x=130, y=250)

    top.mainloop()
    # todo
    quit()
    skip()


def grade_clusters():
    skip()
    global grade_df
    top = Tk()
    top.title("Grade Clusters")
    top.geometry("250x350")

    grades = Label(top, text="Grades", fg='dark green', font="Verdana 10 underline")
    grades.pack()
    grades.place(x=10, y=50)

    grade_a_star = Label(top, text="A*")
    grade_a_star.pack()
    grade_a_star.place(x=30, y=80)

    grade_a = Label(top, text="A")
    grade_a.pack()
    grade_a.place(x=30, y=110)

    grade_b = Label(top, text="B")
    grade_b.pack()
    grade_b.place(x=30, y=140)

    grade_c = Label(top, text="C")
    grade_c.pack()
    grade_c.place(x=30, y=170)

    grade_d = Label(top, text="D")
    grade_d.pack()
    grade_d.place(x=30, y=200)

    min_grade = Label(top, text="Min Grade", fg='dark green', font="Verdana 10 underline")
    min_grade.pack()
    min_grade.place(x=70, y=50)

    min_grade = Label(top, text="Max Grade", fg='dark green', font="Verdana 10 underline")
    min_grade.pack()
    min_grade.place(x=150, y=50)

    global a_star_min_grade
    a_star_min_grade = StringVar()
    a_star_min = Entry(top, textvariable=a_star_min_grade)
    a_star_min.insert(INSERT, grade_df.iloc[0]['MIN_GPA'])
    a_star_min.pack()
    a_star_min.place(x=75, y=80, width=40)

    global a_star_max_grade
    a_star_max_grade = StringVar()
    a_star_max = Entry(top, textvariable=a_star_max_grade)
    a_star_max.insert(INSERT, grade_df.iloc[0]['MAX_GPA'])
    a_star_max.pack()
    a_star_max.place(x=155, y=80, width=40)

    global a_min_grade
    a_min_grade = StringVar()
    a_min = Entry(top, textvariable=a_min_grade)
    a_min.insert(INSERT, grade_df.iloc[1]['MIN_GPA'])
    a_min.pack()
    a_min.place(x=75, y=110, width=40)

    global a_max_grade
    a_max_grade = StringVar()
    a_max = Entry(top, textvariable=a_max_grade)
    a_max.insert(INSERT, grade_df.iloc[1]['MAX_GPA'])
    a_max.pack()
    a_max.place(x=155, y=110, width=40)

    global b_min_grade
    b_min_grade = StringVar()
    b_min = Entry(top, textvariable=b_min_grade)
    b_min.insert(INSERT, grade_df.iloc[2]['MIN_GPA'])
    b_min.pack()
    b_min.place(x=75, y=140, width=40)

    global b_max_grade
    b_max_grade = StringVar()
    b_max = Entry(top, textvariable=b_max_grade)
    b_max.insert(INSERT, grade_df.iloc[2]['MAX_GPA'])
    b_max.pack()
    b_max.place(x=155, y=140, width=40)

    global c_min_grade
    c_min_grade = StringVar()
    c_min = Entry(top, textvariable=c_min_grade)
    c_min.insert(INSERT, grade_df.iloc[3]['MIN_GPA'])
    c_min.pack()
    c_min.place(x=75, y=170, width=40)

    global c_max_grade
    c_max_grade = StringVar()
    c_max = Entry(top, textvariable=c_max_grade)
    c_max.insert(INSERT, grade_df.iloc[3]['MAX_GPA'])
    c_max.pack()
    c_max.place(x=155, y=170, width=40)

    global d_min_grade
    d_min_grade = StringVar()
    d_min = Entry(top, textvariable=d_min_grade)
    d_min.insert(INSERT, grade_df.iloc[4]['MIN_GPA'])
    d_min.pack()
    d_min.place(x=75, y=200, width=40)

    global d_max_grade
    d_max_grade = StringVar()
    d_max = Entry(top, textvariable=d_max_grade)
    d_max.insert(INSERT, grade_df.iloc[4]['MAX_GPA'])
    d_max.pack()
    d_max.place(x=155, y=200, width=40)

    B1 = Button(top, text="Cancel", command=restart_app, fg='White', bg='dark green', height=1, width=10)
    B1.pack()
    B1.place(x=30, y=250)

    B2 = Button(top, text="Save", command=save_grade_clusters, fg='White', bg='dark green', height=1, width=10)
    B2.pack()
    B2.place(x=130, y=250)

    top.mainloop()
    # todo
    quit()
    skip()


############################################################################################
# DB connection § create data frame consist of keywords &


connection = pymysql.connect(host='mysql_db',
                             user='user',
                             password='password',
                             db='graduate',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
'''
connection = mysql.connector.connect(host='localhost',
                             user='user',
                             password='password',
                             database ='graduate',
                             auth_plugin='mysql_native_password')

'''
# gets keywords and corresponding university name from database and assigns into data frame

keywords_sql = "SELECT K.KEYWORD, U.NAME, U.CLUSTER FROM UNIVERSITY U, KEYWORD K WHERE K.UNIVERSITY_ID= U.id"

grade_sql = "SELECT GRADE, MIN_GPA, MAX_GPA FROM GRADE_CLUSTER"

requirements_sql = "SELECT ALES_MIN, GRE_MIN, YDS_MIN, IELTS_OVERALL_MIN, IELTS_WRITE_MIN, " \
                   "TOEFL_OVERALL_MIN, TOEFL_WRITE_MIN FROM REQUIREMENTS"

keyword_df = pd.read_sql(keywords_sql, connection)

grade_df = pd.read_sql(grade_sql, connection)

requirements_df = pd.read_sql(requirements_sql, connection)

############################################################################################
# Get applicant list from excel files selected by user.

file_path = ''

top = Tk()
top.title("Graduate Applications")
top.geometry("400x400")

L1 = Label(top, text="Please select application files (in '.xlsx' extention) ")
L1.pack()
L1.place(x=10, y=90)

L2 = Label(top, text="Multiple selection is possible.")
L2.pack()
L2.place(x=10, y=110)

B1 = Button(top, text="Select Files", command=get_files, fg='White', bg='dark green', height=1, width=10)
B1.pack()
B1.place(x=50, y=200)

B2 = Button(top, text="Grade Clusters", command=grade_clusters, fg='White', bg='dark green', height=1, width=10)
B2.pack()
B2.place(x=150, y=200)

B3 = Button(top, text="Requirements", command=requirements, fg='White', bg='dark green',  height=1, width=10)
B3.pack()
B3.place(x=250, y=200)

top.mainloop()
frames = [pd.read_excel(i, sheet_name=0, skiprows=1) for i in file_path]
df = pd.concat(frames, ignore_index=True)

######### creation year of the first file will be considered.
# Exams valid until the end of the file creation year will be considered as valid.


workbook = xlrd.open_workbook(file_path[0])
worksheet = workbook.sheet_by_index(0)

created_at = worksheet.cell(0, 1).value
# get the created year of the excel file
create_year = int(re.search(r"(\d{4})", created_at).group(1))
# last day of the year file created.
create_date = datetime.date(create_year, 12, 31)

#####################################################################

columns_to_remove = ['PhD Following UGRAD', 'Applied Department', 'Evaluation Status', 'National ID', 'Boun ID',
                     'Home Address', 'Contact Address', 'ALES Verb.', 'ALES Weigh.', 'GRE Verb', 'GRE AWA',
                     'GMAT Exam Date',
                     'GMAT Quan', 'GMAT Verb', 'GMAT Total', 'GMAT AWA', 'IELTS Listen', 'IELTS Read', 'IELTS Speak',
                     'TOEFL IBT Listen', 'TOEFL IBT Read', 'TOEFL IBT Speak', 'BUEPT Listen', 'BUEPT Read']

df.drop(columns_to_remove, axis=1, inplace=True)

# insert UnderGrad Department Type column

ugd = df.columns.get_loc('UGrad Department')

df.insert(ugd + 1, 'UGrad Department Type', '')

df['UGrad Department Type'] = df.apply(lambda row: ugrad_department(row), axis=1)

# insert UnderGrad Second Department Type column

ugsd = df.columns.get_loc('UGrad Second Dept')

df.insert(ugsd + 1, 'UGrad Second Dept Type', '')

df['UGrad Second Dept Type'] = df.apply(lambda row: ugrad_second_department(row), axis=1)

df['UGrad Second Dept Type'] = df.apply(lambda row: ugrad_second_department(row), axis=1)

# insert Grad Program Type column

gp = df.columns.get_loc('Grad Program')

df.insert(gp + 1, 'Grad Program Type', '')

df['Grad Program Type'] = df.apply(lambda row: grad_program(row), axis=1)

############################################################################################
# grade separation

# insert Grade column -- will be removed

ug_cgpa = df.columns.get_loc('UGrad CGPA')

# grade

df.insert(ug_cgpa + 1, 'Normalized UGrad CGPA Grade', '')

df['Normalized UGrad CGPA Grade'] = df.apply(lambda row: get_grade(row), axis=1)

# grading scale

df.insert(ug_cgpa + 2, 'UGrad CGPA Grade Scale', '')

df['UGrad CGPA Grade Scale'] = df.apply(lambda row: get_grade_scale(row), axis=1)

Ugrad_Grade_Changed = df['UGrad CGPA Grade Scale']

# swap if grade and grade scale is entered incorrectly
# and
# grade conversion

for i, row in df.iterrows():
    grade = df.iloc[i]['Normalized UGrad CGPA Grade']
    grade_scale = df.iloc[i]['UGrad CGPA Grade Scale']

    if grade > grade_scale:
        new_grade = grade_scale
        new_grade_scale = grade
        df.at[i, 'Normalized UGrad CGPA Grade'] = new_grade
        df.at[i, 'UGrad CGPA Grade Scale'] = new_grade_scale
        grade = new_grade
        grade_scale = new_grade_scale
    if grade_scale == 4:
        Ugrad_Grade_Changed.at[i] = 0
        continue
    if grade_scale == 5:
        grade = round(grade * 0.8, 2)
        df.at[i, 'Normalized UGrad CGPA Grade'] = grade
        Ugrad_Grade_Changed.at[i] = 1
        continue
    if grade_scale == 100:
        grade = round((((grade * 3) - 20) / 70), 2)
        df.at[i, 'Normalized UGrad CGPA Grade'] = grade
        Ugrad_Grade_Changed.at[i] = 1
        continue

    ######## 20 is converted to 100 and then to 4.
    if grade_scale == 20:
        grade = round((((grade * 15) - 20) / 70), 2)
        df.at[i, 'Normalized UGrad CGPA Grade'] = grade
        Ugrad_Grade_Changed.at[i] = 1

ug_grade_scale = df.columns.get_loc('UGrad CGPA Grade Scale')

# first assign default value to all (for now, "F" is assigned, can be changed.)
df.insert(ug_grade_scale + 1, 'UGrad Grade Cluster', 'F')

# decide grade scale

for i, row in df.iterrows():
    grade = df.iloc[i]['Normalized UGrad CGPA Grade']
    for j in range(0, len(grade_df)):
        min_gpa = grade_df.iloc[j]['MIN_GPA']
        max_gpa = grade_df.iloc[j]['MAX_GPA']
        if grade >= min_gpa and grade <= max_gpa:
            df.at[i, 'UGrad Grade Cluster'] = grade_df.iloc[j]['GRADE']
            continue

############################################################################################
# keyword recognition and data correction
# and
# university cluster


unknown_universities = []

ug_university = df.columns.get_loc('UGrad University')

df.insert(ug_university + 1, 'UGrad University Cluster', '')

for i, row in df.iterrows():
    ugrad_uni = df.iloc[i]['UGrad University']
    grad_uni = df.iloc[i]['Grad University']
    ugrad_uni_cluster = 'XX'
    ugrad_uni = replace_turkish_characters(ugrad_uni)
    grad_uni = replace_turkish_characters(grad_uni)
    ugrad_found = 0
    grad_found = 0
    for j in range(0, len(keyword_df)):
        keyword = keyword_df.iloc[j][0]
        if ugrad_uni.find(keyword) >= 0:
            ugrad_uni = keyword_df.iloc[j][1]
            ugrad_uni_cluster = keyword_df.iloc[j][2]
            ugrad_found = 1
        if grad_uni.find(keyword) >= 0:
            grad_uni = keyword_df.iloc[j][1]
            grad_found = 1
        if ugrad_found == 1 and grad_found == 1:
            break
    if ugrad_found == 0 and len(ugrad_uni) > 0:
        if ugrad_uni not in unknown_universities:
            unknown_universities.append(ugrad_uni)

    if grad_found == 0 and len(grad_uni) > 0:
        if grad_uni not in unknown_universities:
            unknown_universities.append(grad_uni)

    df.at[i, 'UGrad University'] = ugrad_uni
    df.at[i, 'Grad University'] = grad_uni
    df.at[i, 'UGrad University Cluster'] = ugrad_uni_cluster

for i in unknown_universities:
    enter = 0

    top = Tk()
    top.title("Unknown University")
    top.geometry("800x300")
    text1 = "Do you want to enter keywords for " + i + " ?"
    L1 = Label(top, text=text1)
    L1.pack()
    L1.place(x=10, y=60)

    B1 = Button(top, text="Skip", command=skip, fg='White', bg='dark green', height=1, width=10)
    B1.pack()
    B1.place(x=200, y=200)

    B2 = Button(top, text="Yes", command=keyword_entry, fg='White', bg='dark green', height=1, width=10)
    B2.pack()
    B2.place(x=100, y=200)

    top.mainloop()

    if (enter == 1):
        li = []
        uni_name = ''

        top = Tk()
        top.title("Graduate Applications")
        top.geometry("600x500")
        text1 = "Please enter (substring) keywords for " + i + " :"

        L1 = Label(top, text=text1)
        L1.pack()
        L1.place(x=10, y=40)

        L_uni = Label(top, text="University Name:")
        L_uni.pack()
        L_uni.place(x=10, y=80)

        Uni_box = Entry(top)
        Uni_box.insert(INSERT, i)
        Uni_box.pack()
        Uni_box.place(x=130, y=80, width=300)

        L_uni = Label(top, text="(Can be changed)")
        L_uni.pack()
        L_uni.place(x=440, y=80)

        L_uni_cluster = Label(top, text="University Cluster:")
        L_uni_cluster.pack()
        L_uni_cluster.place(x=10, y=120)

        variable = StringVar(top)
        variable.set("Other")  # default value
        Uni_Cluster_Menu = OptionMenu(top, variable, "Other", "A1", "A2", "B1", "B2")
        Uni_Cluster_Menu.pack()
        Uni_Cluster_Menu.place(x=130, y=120)

        L1 = Label(top, text="Keyword 1:")
        L1.pack()
        L1.place(x=10, y=180)

        K1 = Entry(top)
        K1.pack()
        K1.place(x=130, y=180, width=200)

        L12 = Label(top, text="(mandatory)")
        L12.pack()
        L12.place(x=350, y=180)

        L2 = Label(top, text="Keyword 2:")
        L2.pack()
        L2.place(x=10, y=220)

        K2 = Entry(top)
        K2.pack()
        K2.place(x=130, y=220, width=200)

        L22 = Label(top, text="(optional)")
        L22.pack()
        L22.place(x=350, y=220)

        L3 = Label(top, text="Keyword 3:")
        L3.pack()
        L3.place(x=10, y=260)

        K3 = Entry(top)
        K3.pack()
        K3.place(x=130, y=260, width=200)

        L32 = Label(top, text="(optional)")
        L32.pack()
        L32.place(x=350, y=260)

        L4 = Label(top, text="Keyword 4:")
        L4.pack()
        L4.place(x=10, y=300)

        K4 = Entry(top)
        K4.pack()
        K4.place(x=130, y=300, width=200)

        L42 = Label(top, text="(optional)")
        L42.pack()
        L42.place(x=350, y=300)

        L5 = Label(top, text="Keyword 5:")
        L5.pack()
        L5.place(x=10, y=340)

        K5 = Entry(top)
        K5.pack()
        K5.place(x=130, y=340, width=200)

        L52 = Label(top, text="(optional)")
        L52.pack()
        L52.place(x=350, y=340)

        B1 = Button(top, text="Cancel", command=skip, fg='White', bg='dark green', height=1, width=10)
        B1.pack()
        B1.place(x=200, y=390)

        B2 = Button(top, text="Save", command=save_and_print, fg='White', bg='dark green', height=1, width=10)
        B2.pack()
        B2.place(x=350, y=390)

        top.mainloop()

############################################################################################
# deciding groups according to grade, university and department clusters

df.insert(0, 'Group', '')

for i, row in df.iterrows():
    uni = df.iloc[i]['UGrad University']
    uni_cluster = df.iloc[i]['UGrad University Cluster']
    grade_cluster = df.iloc[i]['UGrad Grade Cluster']
    department_type = df.iloc[i]['UGrad Department Type']

    if ((uni == 'BOGAZICI UNIVERSITESI' and department_type == 'CMPE OR SIMILAR')
            or (grade_cluster == 'A*' or grade_cluster == 'A')
            or (grade_cluster == 'B' and uni_cluster == 'A1')
            or (grade_cluster == 'B' and uni_cluster == 'A2' and department_type == 'CMPE OR SIMILAR')
            or (grade_cluster == 'B' and uni_cluster == 'B1' and department_type == 'CMPE OR SIMILAR')
            or (grade_cluster == 'C' and uni_cluster == 'A1' and department_type == 'CMPE OR SIMILAR')):
        df.at[i, 'Group'] = 'Group_1'


    elif ((grade_cluster == 'D' and department_type == 'OTHER')
          or (grade_cluster == 'F')
          or (grade_cluster == 'D' and uni_cluster == 'XX' and department_type == 'CMPE OR SIMILAR')
          or (grade_cluster == 'C' and uni_cluster == 'B2' and department_type == 'OTHER')
          or (grade_cluster == 'C' and uni_cluster == 'XX' and department_type == 'OTHER')):
        df.at[i, 'Group'] = 'Group_3'
    else:
        df.at[i, 'Group'] = 'Group_2'

############################################################################################
# insert requirements (sufficiency) columns


group_column = df.columns.get_loc('Group')

df.insert(group_column + 1, 'English Proficiency', '0')

df.insert(group_column + 2, 'Ales - GRE Proficiency', '0')  # ismi değişecek

df.insert(group_column + 3, 'YDS Proficiency', 0)

df.insert(group_column + 4, 'Overall_Status', 0)  # ismi değişecek

for i, row in df.iterrows():
    # max 2 years of last boğaziçi graduation
    ugrad_uni = df.iloc[i]['UGrad University']
    ugrad_grad_date = df.iloc[i]['UGrad Graduation Date']
    grad_uni = df.iloc[i]['Grad University']
    grad_grad_date = df.iloc[i]['Grad Graduation Date']

    # 2 years,  overall min 6.5 , write min 6.5
    ielts_overall = df.iloc[i]['IELTS Overall']
    ielts_write = df.iloc[i]['IELTS Write']
    ielts_exam_date = df.iloc[i]['IELTS Exam Date']

    # 2 years,  overall min 79, write min 22
    toefl_ibt_overall = df.iloc[i]['TOEFL IBT Overall']
    toefl_ibt_write = df.iloc[i]['TOEFL IBT Write']
    toefl_ibt_exam_date = df.iloc[i]['TOEFL IBT Exam Date']

    # 2 years,  overall A,B or C, write S??
    buept_overall = df.iloc[i]['BUEPT Overall']
    buept_write = df.iloc[i]['BUEPT Write']
    buept_exam_date = df.iloc[i]['BUEPT Exam Date']

    # 3 years,  quantitive min 85
    ales_quantitative = df.iloc[i]['ALES Quan.']
    ales_exam_date = df.iloc[i]['ALES Exam Date']

    # 3 years,  quantitive min 165
    gre_quantitative = df.iloc[i]['GRE Quan']
    gre_exam_date = df.iloc[i]['GRE Exam Date']

    # 5 years,  min 55
    yds_total = df.iloc[i]['YDS Total']
    yds_exam_date = df.iloc[i]['YDS Exam Date']

    # prep class
    prep = df.iloc[i]['Preparatory Class']

    # todo: tarih karşılaştırma gelecek.

    # english proficiency

    if grad_uni == 'BOGAZICI UNIVERSITESI':
        grad_year = int(grad_grad_date[-4:])

        if create_year - 2 < grad_year:
            df.at[i, 'English Proficiency'] = 'boun-grad'

    elif ugrad_uni == 'BOGAZICI UNIVERSITESI':
        ugrad_year = int(ugrad_grad_date[-4:])

        if create_year - 2 < ugrad_year:
            df.at[i, 'English Proficiency'] = 'boun - ugrad'

    if ielts_overall >= requirements_df.iloc[0]['IELTS_OVERALL_MIN'] \
            and ielts_write >= requirements_df.iloc[0]['IELTS_WRITE_MIN']:
        ielts_year = int(ielts_exam_date[-4:])

        if create_year - 2 < ielts_year:
            df.at[i, 'English Proficiency'] = 'ielts'

    if toefl_ibt_overall >= requirements_df.iloc[0]['TOEFL_OVERALL_MIN'] \
            and toefl_ibt_write >= requirements_df.iloc[0]['TOEFL_WRITE_MIN']:
        toefl_ibt_year = int(toefl_ibt_exam_date[-4:])

        if create_year - 2 < toefl_ibt_year:
            df.at[i, 'English Proficiency'] = 'toefl'

    if (buept_overall == 'A' or buept_overall == 'B' or buept_overall == 'C') and buept_write == 'S':
        buept_year = int(buept_exam_date[-4:])

        if create_year - 2 < buept_year:
            df.at[i, 'English Proficiency'] = 'buept'

    # ales or gre
    if ales_quantitative >= requirements_df.iloc[0]['ALES_MIN']:
        ales_year = int(ales_exam_date[-4:])

        if create_year - 3 < ales_year:
            df.at[i, 'Ales - GRE Proficiency'] = 'ales'
    if gre_quantitative >= requirements_df.iloc[0]['GRE_MIN']:
        gre_year = int(gre_exam_date[-4:])

        if create_year - 3 < gre_year:
            df.at[i, 'Ales - GRE Proficiency'] = 'gre'

    # yds

    if yds_total >= requirements_df.iloc[0]['YDS_MIN']:

        yds_year = int(yds_exam_date[-4:])

        if create_year - 5 < yds_year:
            df.at[i, 'YDS Proficiency'] = 1

    # Overall_Status
    if df.iloc[i]['Ales - GRE Proficiency'] != '0':
        if df.iloc[i]['Program'] == 'BİLGİSAYAR MÜHENDİSLİĞİ (MASTER)' or df.iloc[i]['YDS Proficiency'] != 0:
            if df.iloc[i]['English Proficiency'] != '0':
                df.at[i, 'Overall_Status'] = 2
            elif df.iloc[i]['Preparatory Class'] == 'YES':
                df.at[i, 'Overall_Status'] = 1

df.sort_values(['Overall_Status'], ascending=False, inplace=True)

############################################################################################
# write data to different excel files


# getting only program=MASTER rows
master_df = df.loc[df.Program == 'BİLGİSAYAR MÜHENDİSLİĞİ (MASTER)'].copy()

# remove PHD related columns from MASTER file

columns_to_remove_from_master = ['YDS Exam Date', 'YDS Total', 'YDS Proficiency']

master_df.drop(columns_to_remove_from_master, axis=1, inplace=True)

# grouping

group_1_df = master_df[master_df.Group == 'Group_1']

group_2_df = master_df[master_df.Group == 'Group_2']

group_3_df = master_df[master_df.Group == 'Group_3']

# getting only program=PHD rows
phd_df = df.loc[df.Program == 'BİLGİSAYAR MÜHENDİSLİĞİ (PHD)'].copy()

# insert Supporting Advisor column for PHD file

phd_df.insert(0, 'Supporting Advisor', '')

phd_excel = pd.ExcelWriter('applicant_phd.xlsx', engine='xlsxwriter')
phd_df.to_excel(phd_excel, sheet_name='PhD Applicants', header=True, index=False)

# master groups into different sheets

master_group_excel = pd.ExcelWriter('master_groups.xlsx', engine='xlsxwriter')

group_1_df.to_excel(master_group_excel, sheet_name='Group 1', header=True, index=False)
group_2_df.to_excel(master_group_excel, sheet_name='Group 2', header=True, index=False)
group_3_df.to_excel(master_group_excel, sheet_name='Group 3', header=True, index=False)

############################################################################################
# Highlight (color red) processed grades etc.


# reading excel files for formatting

# Master workbook

ms_workbook = master_group_excel.book
ms_g1_sheet = master_group_excel.sheets['Group 1']
ms_g2_sheet = master_group_excel.sheets['Group 2']
ms_g3_sheet = master_group_excel.sheets['Group 3']

# PhD workbook
phd_workbook = phd_excel.book
phd_sheet = phd_excel.sheets['PhD Applicants']

# setting format for processed cells to highlight
# ms
format1 = ms_workbook.add_format()
format1.set_font_color('red')

# phd
format2 = phd_workbook.add_format()
format2.set_font_color('red')

# for Group 1 Sheet

# get grade cluster column's location
grade_cluster_column = group_1_df.columns.get_loc('UGrad Grade Cluster')

# red for converted grades

for i, row in group_1_df.iterrows():
    j = group_1_df.index.get_loc(i)
    grade_scale = group_1_df.iloc[j]['UGrad CGPA Grade Scale']
    if (grade_scale != 4):
        grade_cluster = group_1_df.iloc[j]['UGrad Grade Cluster']

        ms_g1_sheet.write(j + 1, grade_cluster_column, grade_cluster, format1)

# for Group 2 Sheet

# get grade cluster column's location
grade_cluster_column = group_2_df.columns.get_loc('UGrad Grade Cluster')

# red for converted grades

for i, row in group_2_df.iterrows():
    j = group_2_df.index.get_loc(i)
    grade_scale = group_2_df.iloc[j]['UGrad CGPA Grade Scale']
    if grade_scale != 4:
        grade_cluster = group_2_df.iloc[j]['UGrad Grade Cluster']
        ms_g2_sheet.write(j + 1, grade_cluster_column, grade_cluster, format1)

# for Group 3 Sheet

# get grade cluster column's location
grade_cluster_column = group_3_df.columns.get_loc('UGrad Grade Cluster')

for i, row in group_3_df.iterrows():
    j = group_3_df.index.get_loc(i)
    grade_scale = group_3_df.iloc[j]['UGrad CGPA Grade Scale']
    if grade_scale != 4:
        grade_cluster = group_3_df.iloc[j]['UGrad Grade Cluster']
        ms_g3_sheet.write(j + 1, grade_cluster_column, grade_cluster, format1)

# for PHD Sheet

# get grade cluster column's location
grade_cluster_column = phd_df.columns.get_loc('UGrad Grade Cluster')

for i, row in phd_df.iterrows():
    j = phd_df.index.get_loc(i)
    grade_scale = phd_df.iloc[j]['UGrad CGPA Grade Scale']
    if grade_scale != 4:
        grade_cluster = phd_df.iloc[j]['UGrad Grade Cluster']
        phd_sheet.write(j + 1, grade_cluster_column, grade_cluster, format2)

master_group_excel.save()
phd_excel.save()

top = Tk()
top.title("Analysis of Graduate Applications")
top.geometry("900x500")
text1 = "Analysis is completed."

L1 = Label(top, text=text1)
L1.pack()
L1.place(x=10, y=60)

L2 = Label(top, text="Excel files for PHD Applicants and Master Applicants are created.")
L2.pack()
L2.place(x=10, y=80)

PHD_Label = Label(top, text="PHD", fg='dark blue', font="Verdana 10 underline")
PHD_Label.pack()
PHD_Label.place(x=112, y=110)

PHD_Label2 = Label(top, text="2")
PHD_Label2.pack()
PHD_Label2.place(x=73, y=140)

PHD_Label1 = Label(top, text="1")
PHD_Label1.pack()
PHD_Label1.place(x=113, y=140)

PHD_Label0 = Label(top, text="0")
PHD_Label0.pack()
PHD_Label0.place(x=153, y=140)

PHD_LabelA = Label(top, text="Group 1")
PHD_LabelA.pack()
PHD_LabelA.place(x=10, y=165)

PHD_LabelB = Label(top, text="Group 2")
PHD_LabelB.pack()
PHD_LabelB.place(x=10, y=195)

PHD_LabelC = Label(top, text="Group 3")
PHD_LabelC.pack()
PHD_LabelC.place(x=10, y=225)

phd_1_2 = len(phd_df[(phd_df['Group'] == 'Group_1') & (phd_df['Overall_Status'] == 2)])

PHD_Entry_12 = Entry(top)
PHD_Entry_12.pack()
PHD_Entry_12.place(x=70, y=165, width=30)
PHD_Entry_12.insert(INSERT, phd_1_2)
PHD_Entry_12.config(state=DISABLED)

phd_1_1 = len(phd_df[(phd_df['Group'] == 'Group_1') & (phd_df['Overall_Status'] == 1)])

PHD_Entry_11 = Entry(top)
PHD_Entry_11.pack()
PHD_Entry_11.place(x=110, y=165, width=30)
PHD_Entry_11.insert(INSERT, phd_1_1)
PHD_Entry_11.config(state=DISABLED)

phd_1_0 = len(phd_df[(phd_df['Group'] == 'Group_1') & (phd_df['Overall_Status'] == 0)])

PHD_Entry_10 = Entry(top)
PHD_Entry_10.pack()
PHD_Entry_10.place(x=150, y=165, width=30)
PHD_Entry_10.insert(INSERT, phd_1_0)
PHD_Entry_10.config(state=DISABLED)

phd_2_2 = len(phd_df[(phd_df['Group'] == 'Group_2') & (phd_df['Overall_Status'] == 2)])

PHD_Entry_22 = Entry(top)
PHD_Entry_22.pack()
PHD_Entry_22.place(x=70, y=195, width=30)
PHD_Entry_22.insert(INSERT, phd_2_2)
PHD_Entry_22.config(state=DISABLED)

phd_2_1 = len(phd_df[(phd_df['Group'] == 'Group_2') & (phd_df['Overall_Status'] == 1)])

PHD_Entry_21 = Entry(top)
PHD_Entry_21.pack()
PHD_Entry_21.place(x=110, y=195, width=30)
PHD_Entry_21.insert(INSERT, phd_2_1)
PHD_Entry_21.config(state=DISABLED)

phd_2_0 = len(phd_df[(phd_df['Group'] == 'Group_2') & (phd_df['Overall_Status'] == 0)])

PHD_Entry_20 = Entry(top)
PHD_Entry_20.pack()
PHD_Entry_20.place(x=150, y=195, width=30)
PHD_Entry_20.insert(INSERT, phd_2_0)
PHD_Entry_20.config(state=DISABLED)

phd_3_2 = len(phd_df[(phd_df['Group'] == 'Group_3') & (phd_df['Overall_Status'] == 2)])

PHD_Entry_32 = Entry(top)
PHD_Entry_32.pack()
PHD_Entry_32.place(x=70, y=225, width=30)
PHD_Entry_32.insert(INSERT, phd_3_2)
PHD_Entry_32.config(state=DISABLED)

phd_3_1 = len(phd_df[(phd_df['Group'] == 'Group_3') & (phd_df['Overall_Status'] == 1)])

PHD_Entry_31 = Entry(top)
PHD_Entry_31.pack()
PHD_Entry_31.place(x=110, y=225, width=30)
PHD_Entry_31.insert(INSERT, phd_3_1)
PHD_Entry_31.config(state=DISABLED)

phd_3_0 = len(phd_df[(phd_df['Group'] == 'Group_3') & (phd_df['Overall_Status'] == 0)])

PHD_Entry_30 = Entry(top)
PHD_Entry_30.pack()
PHD_Entry_30.place(x=150, y=225, width=30)
PHD_Entry_30.insert(INSERT, phd_3_0)
PHD_Entry_30.config(state=DISABLED)

MS_Label = Label(top, text="MS", fg='dark blue', font="Verdana 10 underline")
MS_Label.pack()
MS_Label.place(x=353, y=110)

MS_Label2 = Label(top, text="2")
MS_Label2.pack()
MS_Label2.place(x=313, y=140)

MS_Label1 = Label(top, text="1")
MS_Label1.pack()
MS_Label1.place(x=353, y=140)

MS_Label0 = Label(top, text="0")
MS_Label0.pack()
MS_Label0.place(x=393, y=140)

MS_LabelA = Label(top, text="Group 1")
MS_LabelA.pack()
MS_LabelA.place(x=250, y=165)

MS_LabelB = Label(top, text="Group 2")
MS_LabelB.pack()
MS_LabelB.place(x=250, y=195)

MS_LabelC = Label(top, text="Group 3")
MS_LabelC.pack()
MS_LabelC.place(x=250, y=225)

ms_1_2 = len(master_df[(master_df['Group'] == 'Group_1') & (master_df['Overall_Status'] == 2)])

MS_Entry_12 = Entry(top)
MS_Entry_12.pack()
MS_Entry_12.place(x=310, y=165, width=30)
MS_Entry_12.insert(INSERT, ms_1_2)
MS_Entry_12.config(state=DISABLED)

ms_1_1 = len(master_df[(master_df['Group'] == 'Group_1') & (master_df['Overall_Status'] == 1)])

MS_Entry_11 = Entry(top)
MS_Entry_11.pack()
MS_Entry_11.place(x=350, y=165, width=30)
MS_Entry_11.insert(INSERT, ms_1_1)
MS_Entry_11.config(state=DISABLED)

ms_1_0 = len(master_df[(master_df['Group'] == 'Group_1') & (master_df['Overall_Status'] == 0)])

MS_Entry_10 = Entry(top)
MS_Entry_10.pack()
MS_Entry_10.place(x=390, y=165, width=30)
MS_Entry_10.insert(INSERT, ms_1_0)
MS_Entry_10.config(state=DISABLED)

ms_2_2 = len(master_df[(master_df['Group'] == 'Group_2') & (master_df['Overall_Status'] == 2)])

MS_Entry_22 = Entry(top)
MS_Entry_22.pack()
MS_Entry_22.place(x=310, y=195, width=30)
MS_Entry_22.insert(INSERT, ms_2_2)
MS_Entry_22.config(state=DISABLED)

ms_2_1 = len(master_df[(master_df['Group'] == 'Group_2') & (master_df['Overall_Status'] == 1)])

MS_Entry_21 = Entry(top)
MS_Entry_21.pack()
MS_Entry_21.place(x=350, y=195, width=30)
MS_Entry_21.insert(INSERT, ms_2_1)
MS_Entry_21.config(state=DISABLED)

ms_2_0 = len(master_df[(master_df['Group'] == 'Group_2') & (master_df['Overall_Status'] == 0)])

MS_Entry_20 = Entry(top)
MS_Entry_20.pack()
MS_Entry_20.place(x=390, y=195, width=30)
MS_Entry_20.insert(INSERT, ms_2_0)
MS_Entry_20.config(state=DISABLED)

ms_3_2 = len(master_df[(master_df['Group'] == 'Group_3') & (master_df['Overall_Status'] == 2)])

MS_Entry_32 = Entry(top)
MS_Entry_32.pack()
MS_Entry_32.place(x=310, y=225, width=30)
MS_Entry_32.insert(INSERT, ms_3_2)
MS_Entry_32.config(state=DISABLED)

ms_3_1 = len(master_df[(master_df['Group'] == 'Group_3') & (master_df['Overall_Status'] == 1)])

MS_Entry_31 = Entry(top)
MS_Entry_31.pack()
MS_Entry_31.place(x=350, y=225, width=30)
MS_Entry_31.insert(INSERT, ms_3_1)
MS_Entry_31.config(state=DISABLED)

ms_3_0 = len(master_df[(master_df['Group'] == 'Group_3') & (master_df['Overall_Status'] == 0)])

MS_Entry_30 = Entry(top)
MS_Entry_30.pack()
MS_Entry_30.place(x=390, y=225, width=30)
MS_Entry_30.insert(INSERT, ms_3_0)
MS_Entry_30.config(state=DISABLED)

L3 = Label(top, text="Student Clusters (Group 1, Group 2 , Group 3)")
L3.pack()
L3.place(x=470, y=160)

L4 = Label(top, text="(According to University, Department and GPA)")
L4.pack()
L4.place(x=470, y=190)

L5 = Label(top, text="Group 1 > Group 2 > Group 3")
L5.pack()
L5.place(x=470, y=220)

L6 = Label(top, text="Required Exam Clusters")
L6.pack()
L6.place(x=470, y=270)

L7 = Label(top, text="2: All required exams are OK")
L7.pack()
L7.place(x=470, y=300)

L8 = Label(top, text="1: All required exams except English are OK. Prep Class is accepted.")
L8.pack()
L8.place(x=470, y=330)

L9 = Label(top, text="0: At least one required exam is missing.")
L9.pack()
L9.place(x=470, y=360)

B1 = Button(top, text="Close", command=skip, fg='White', bg='dark green', height=1, width=10)
B1.pack()
B1.place(x=550, y=400)
top.mainloop()
