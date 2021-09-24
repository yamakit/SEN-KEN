from decimal import Decimal
from PIL import Image
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
cur.execute("SELECT video_path, frame1, x_coordinate, y_coordinate FROM yolo_video_table WHERE ball_id = 1 and yolo_flag = 2")
rows = cur.fetchall()
folder = []
folder1 = []
print(rows)
for row in rows:
    folder.append(row[0])
    folder1.append(row[1])
cur.close
conn.commit()
conn.close()


print(folder)
ball_id = 2 # バレー:1 バド:2 テニス:3
player_id = 1 # DBを参照
rep_chk = 0

im = Image.open('../2021SEN_KEN/volleyball/01/ffmpeg_0566/000001.jpg')
croped = im.crop((318, 224, 493, 398))
croped.save('./' + 'cake.jpg')
# folder = ['D:\\htdocs\\SEN-KEN\\2021SEN_KEN\\volleyball\\02\\2106041922040.MOV']

# print(folder)

for path, frame1 in zip(folder, folder1):
    print(path + 'を処理中...')
    print(path, frame1)
    frame1 = str(frame1)
    #PATHを文字列連結に変更するところから
    frame1_zero = frame1.zfill(5)
    print(frame1_zero)    
    file_name = path.replace(".MOV","")
    print(file_name)

    file_names = file_name.replace("../", "D:/htdocs/")
    file_names = file_names.replace("D:/htdocs/SEN-KEN/2021SEN_KEN/volleyball/","")    
    person_num = file_names[:2]
    print(person_num)
    video_num = file_names[3:]
    print(video_num)

    resutl = subprocess.run(['picture.bat', person_num, video_num, frame1_zero], shell=True)

    conn = mydb.connect(host='localhost',port='3306',user='root',password='',database='SEN-KEN')
    cur = conn.cursor(buffered=True)
    cur.execute(f"UPDATE yolo_video_table SET yolo_flag = 3 WHERE video_path = '{path}'")
    cur.close
    conn.commit()
    conn.close()