import glob as gb
import mysql.connector as mydb
import os

<<<<<<< HEAD
files = gb.glob("D:\\2021SEN_KEN\\volleyball\\*\\*.json")
conn = mydb.connect(host='localhost',port='3306',user='root',password='',database='hikaku_test_db')
=======
files = gb.glob('D:\\2021SEN_KEN\\volleyball\\*\\*.MOV')
conn = mydb.connect(host='localhost',port='3306',user='root',password='',database='SEN-KEN')
>>>>>>> 122e549c028126871015384064431ba153c69435

# DB操作用にカーソルを作成
cur = conn.cursor(buffered=True)
cur.execute("SELECT video_path FROM yolo_video_table")
rows = cur.fetchall()

for row in rows:
    row = list(row) 
    if(row[0] in files):
        files.remove(row[0])

<<<<<<< HEAD
for f in files:
    f = f.replace(".json", ".MOV")
    f = f.replace("ffmpeg", "IMG")
    f = f.replace('\\', )
    cur.execute("INSERT yolo_video_table VALUES (%(id)s, %(ans_id)s, %(ball_id)s, %(frame1)s, %(frame2)s, %(player_id)s, %(video_path)s, %(x_coordinate)s, %(y_coordinate)s, %(yolo_flag)s)", {'id':None, 'ans_id':-1, 'ball_id':1, 'frame1':-1, 'frame2':-1, 'player_id':1, 'video_path':f, 'x_coordinate':-1, 'y_coordinate':-1, 'yolo_flag':0})
=======
for file in files:
    cur.execute("INSERT yolo_video_table VALUES (%(id)s, %(ans_id)s, %(ball_id)s, %(frame1)s, %(frame2)s, %(player_id)s, %(x_coordinate)s, %(y_coordinate)s, %(video_path)s, %(yolo_flag)s)", {'id':None, 'ans_id':-1, 'ball_id':1, 'frame1':-1, 'frame2':-1, 'player_id':1, 'video_path':file, 'x_coordinate':-1, 'y_coordinate':-1, 'yolo_flag':0})
>>>>>>> 122e549c028126871015384064431ba153c69435

print(str(files) + ' was uploaded!')

cur.close()
conn.commit()
conn.close()