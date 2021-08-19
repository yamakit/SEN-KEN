import mysql.connector as mydb
import os

conn = mydb.connect(host='localhost',port='3306',user='root',password='',database='test')
cur = conn.cursor(buffered=True)
cur.execute("SELECT video_path,frame1 FROM yolo_video_tables WHERE yolo_flag = 2")
rows = cur.fetchall()
path_lists = [] #目的の画像の連番とそれが入っているフォルダーのパスのリスト群

for row in rows:
    path_lists.append([row[0], row[1]])
cur.close
conn.commit()
conn.close()

for path_list in path_lists:
    folder = path_list[0]
    frame1 = path_list[1]

    folder_path = folder.replace('.MOV', '/')                       #フォルダ化
    folder_path = folder_path.replace('../', 'D:/htdocs/SEN-KEN/')  #フルパス化

    image_num = str(frame1).zfill(6)    #目的の画像に振られる連番に合わせて5桁で0埋め

    image_path = folder_path + image_num + '.jpg' #目的の画像のパスを生成
    print(image_path, end=' ')

    if(os.path.exists(image_path)):
        #---生成したパスをDBに送る---
        conn = mydb.connect(host='localhost',port='3306',user='root',password='',database='sen-ken')
        cur = conn.cursor(buffered=True)
        cur.execute(f"INSERT INTO `picture_table`(`picture_path`,`frame1`) VALUES ('{image_path}',{frame1})")
        cur.close
        conn.commit()
        conn.close()
        print()
    else:
        print('< CannotFoundSuchFile')