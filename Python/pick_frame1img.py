import mysql.connector as mydb
import os

conn = mydb.connect(host='localhost',port='3306',user='root',password='',database='sen-ken')
cur = conn.cursor(buffered=True)
cur.execute("SELECT video_path,frame1,video_id FROM yolo_video_table WHERE 1")
rows = cur.fetchall()
path_lists = [] #目的の画像の連番とそれが入っているフォルダーのパスのリスト群

for row in rows:
    path_lists.append([row[0], row[1], row[2]])
cur.close
conn.commit()
conn.close()

for path_list in path_lists:
    folder = path_list[0]
    frame1 = path_list[1]
    video_id = path_list[2]

    folder_path = folder.replace('.MOV', '/')                       #フォルダ化
    folder_path = folder_path.replace('../', '../')  #フルパス化

    image_num = str(frame1).zfill(6)    #目的の画像に振られる連番に合わせて5桁で0埋め

    image_path = folder_path + image_num + '.jpg' #目的の画像のパスを生成
    print(image_path, end=' ')

    if(os.path.exists(image_path)):
        #---生成したパスをDBに送る---
        conn = mydb.connect(host='localhost',port='3306',user='root',password='',database='sen-ken')
        cur = conn.cursor(buffered=True)
        cur.execute(f"INSERT INTO `picture`(`video_id`,`frame1`, `picture_path`) VALUES ({video_id}, {frame1},'{image_path}')")
        cur.close
        conn.commit()
        conn.close()
        print()
    else:
        print('< CannotFoundSuchFile')
