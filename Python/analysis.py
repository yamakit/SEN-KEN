from decimal import Decimal
from re import T
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
cur.execute("SELECT video_path FROM yolo_video_table WHERE yolo_flag = 0")
rows = cur.fetchall()
folder = []
print(rows)
for row in rows:
    folder.append(row[0])
cur.close
conn.commit()
conn.close()

cmd_file = 'C:\\Users\\procon\\Desktop\\2021SEN-KEN\\YOLOv3_volleyball3.bat'

ball_id = 1 # バレー:1 バド:2 テニス:3
player_id = 1 # DBを参照

# folder = gb.glob("D:\\htdocs\\2021SEN_KEN\\volleyball\\*\\*.json")
rep_chk = 0
print(folder)

for fl in folder:
    print(fl + 'を処理中...')

    file_name = fl.replace(".MOV","")
    video_num = file_name[-4:]
    print(video_num)
    command = cmd_file + " " + video_num
    resutl = subprocess.run(['C:/Users/procon/Desktop/2021SEN-KEN/YOLOv3_volleyball3.bat', video_num], shell=True)

    conn = mydb.connect(host='localhost',port='3306',user='root',password='',database='SEN-KEN')
    cur = conn.cursor(buffered=True)
    cur.execute(f"UPDATE yolo_video_table SET yolo_flag = 1 WHERE video_path = '{fl}'")
    cur.close
    conn.commit()
    conn.close()