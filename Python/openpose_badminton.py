from decimal import Decimal
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pandas.io.json import json_normalize
import mysql.connector as mydb
import glob as gb
import os
import subprocess

conn = mydb.connect(host='localhost',port='3306',user='root',password='',database='SEN-KEN')
cur = conn.cursor(buffered=True)
cur.execute("SELECT video_path FROM yolo_video_table WHERE ball_id = 2 and yolo_flag = 2")
rows = cur.fetchall()
folder = []
print(rows)
for row in rows:
    folder.append(row[0])
cur.close
conn.commit()
conn.close()

ball_id = 1 # バレー:1 バド:2 テニス:3
player_id = 1 # DBを参照
rep_chk = 0
print(folder)

for fl in folder:
    print(fl + 'を処理中...')

    file_name = fl.replace(".MOV","")
    file_names = file_name.replace("../", "D:\\htdocs\\")
    file_names = file_names.replace("D:\\htdocs\\2021SEN_KEN/badminton/", "")
    print(file_names)
    person_num = file_names[:2]
    print(person_num)
    video_num = file_names[3:]
    print(video_num)
    
    resutl = subprocess.run(['OpenPose_badminton.bat', person_num ,video_num], shell=True)


    conn = mydb.connect(host='localhost',port='3306',user='root',password='',database='SEN-KEN')
    cur = conn.cursor(buffered=True)
    cur.execute(f"UPDATE yolo_video_table SET yolo_flag = 3 WHERE video_path = '{fl}'")
    cur.close
    conn.commit()
    conn.close()