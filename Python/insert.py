from decimal import Decimal
from re import T
from numpy.core.numeric import NaN
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pandas.io.json import json_normalize
import mysql.connector as mydb
import glob as gb

ball_id = 1 # バレー:1 バド:2 テニス:3
player_id = 1 # DBを参照

conn = mydb.connect(host='localhost',port='3306',user='root',password='',database='SEN-KEN')
cur = conn.cursor(buffered=True)
cur.execute("SELECT video_path FROM yolo_video_table WHERE yolo_flag = 1 and ball_id = 1")
rows = cur.fetchall()
folder = []
for row in rows:
    folder.append(row[0])
cur.close
conn.commit()
conn.close()

rep_chk = 0
print(folder)

for fl in folder:
    fl = fl.replace('IMG','ffmpeg')
    fl = fl.replace('MOV','json')
    fl = fl.replace('../',"D:\\htdocs\\")
    fl = fl.replace('/',"\\")

    print(fl + 'を処理中...')
    with open(fl, encoding="utf-8") as f:
        data_lines = f.read()
    chr_list = list(data_lines)
    for c in chr_list:
        if(rep_chk == 0 and c == "\\"):
            rep_chk = 1
        elif(rep_chk == 1):
            if(c != "\\"):
                data_lines = data_lines.replace("\\","\\\\")
                with open(fl, encoding="utf-8", mode="w") as f:
                    f.write(data_lines)
            break

    rep_chk = 0
    json_path = fl #頂点を取得するjsonファイル
    csv_path = fl.replace('json','csv')

    #変換したいJSONファイルを読み込む
    df = pd.read_json(json_path)
    df.to_csv(csv_path, encoding='utf-8')

    data = pd.read_csv(csv_path)

    data['center_y'] = np.nan
    data['center_x'] = np.nan
    data['original_y'] = np.nan
    data['original_x'] = np.nan
    data['sabun_y'] = np.nan
    data['vartex_point'] = np.nan
    stack = 0
    cnt = 0
    vartex_cnt = 0
    renzoku = 0
    frame1 = 0
    Zlist = []

    for i in range(1,len(data) - 1):
        triple = '''{}'''.format(data.loc[i,'objects'])
        obj_list = eval(triple)
        print(obj_list)

        # print("-------------------------------")
        # print(data.loc[i-stack,'center_y'])
        # if(obj_list):
        #     print(obj_list[0]['relative_coordinates']['center_y'])
        #     print(data.loc[i-stack,'center_y'] - obj_list[0]['relative_coordinates']['center_y'])
        # else:
        #     print(None)
        #     print(None)
        # print("-------------------------------")
        if obj_list:
            
            data.loc[i,'original_y'] = obj_list[0]['relative_coordinates']['center_y']
            data.loc[i,'original_x'] = obj_list[0]['relative_coordinates']['center_x']
            if(not(np.isnan(data.loc[i-stack,'center_y']))):
                if(-0.02*(int(stack > 2)+1) < data.loc[i-stack,'center_y'] - obj_list[0]['relative_coordinates']['center_y'] and data.loc[i-stack,'center_y'] - obj_list[0]['relative_coordinates']['center_y'] < 0.02*stack):
                    data.loc[i,'center_y'] = obj_list[0]['relative_coordinates']['center_y']
                    stack = 1
                    # print(f"data.loc[{i-stack},'center_y'] is enable!")
                else:
                    stack += 1
                    # print(f"Displacement is too big so data.loc[{i},'center_y'] is disabled.")
            else:
                data.loc[i,'center_y'] = obj_list[0]['relative_coordinates']['center_y']
                data.loc[i,'center_x'] = obj_list[0]['relative_coordinates']['center_x']
                stack += 1
                # print(f"data.loc[{i-stack},'center_y'] is disable!")
        else:
            stack += 1
            # print('no object!')

    ax = data[:].plot('frame_id', 'center_y', c = 'black', zorder = 2, label = 'not interpolated')

    data.loc[:,['center_y']] = data.loc[:,['center_y']].interpolate(axis=0)
    data.loc[:,['center_x']] = data.loc[:,['center_x']].interpolate(axis=0)

    data[:].plot('frame_id', 'center_y', c = 'red', ax = ax, zorder = 1, label = 'interpolated')

    data.loc[:,['original_y']] = data.loc[:,['original_y']].interpolate(axis=0)
    data.loc[:,['original_x']] = data.loc[:,['original_x']].interpolate(axis=0)
    
    ax2 = data[:].plot('frame_id', 'center_y', c = 'red', zorder = 2, label = 'removed outliers')
    data[:].plot('frame_id', 'original_y', c = 'black', zorder = 1, label = 'don\'t removed outliers', ax = ax2)
    plt.show()

    data['MedFilTemp_y'] = data['center_y'].rolling(24, center=True).median()
    data.loc[:,'MedFilTemp_y'] = data.loc[:,['MedFilTemp_y']].interpolate(axis=0,limit_direction='both')
    data['MedFilTemp_x'] = data['center_x'].rolling(24, center=True).median()
    data.loc[:,'MedFilTemp_x'] = data.loc[:,['MedFilTemp_x']].interpolate(axis=0,limit_direction='both')

    for i in range(1,len(data) - 1):
        
        first_y = Decimal(str(data.loc[i,'MedFilTemp_y']))
        second_y = Decimal(str(data.loc[i + 1,'MedFilTemp_y']))
        diff_y = second_y - first_y

        # if(diff_y > Decimal('0.0075')):
        #     diff_y = 0.0075
        # elif(diff_y < Decimal('-0.0075')):
        #     diff_y = -0.0075
        data.loc[i,'sabun_y'] = float(diff_y)

        if(data.loc[i,'sabun_y'] > 0):
            renzoku += 1
        elif(data.loc[i, 'sabun_y'] <= 0 and renzoku > 20):
            renzoku = 0
            vartex_cnt += 1
            if(vartex_cnt==4):
                frame1 = i
                data.loc[frame1-1:frame1+1,'vartex_point'] = data.loc[frame1, 'sabun_y']
        else:
            renzoku = 0

        first_x = Decimal(str(data.loc[i,'MedFilTemp_x']))
        second_x = Decimal(str(data.loc[i + 1,'MedFilTemp_x']))
        diff_x = second_x - first_x
        data.loc[i,'sabun_x'] = float(diff_x)
    ax = data[:].plot('frame_id', 'sabun_y', c = 'red')
    data[:].plot('frame_id', 'vartex_point', c = 'black', ax = ax)
    plt.show()

    #---こっからDB関連---

    # コネクションの作成
    conn = mydb.connect(host='localhost',port='3306',user='root',password='',database='SEN-KEN')

    fl = fl.replace("\\", "/")
    # DB操作用にカーソルを作成
    cur = conn.cursor(buffered=True)
    fl = fl.replace(".json", ".MOV")
    fl = fl.replace("ffmpeg", "IMG")
    fl = fl.replace("D:/htdocs/", "../")
    print(fl)
    if(np.isnan(data.loc[frame1, 'original_x'])):
        data.loc[frame1, 'original_x'] = -1
    if(np.isnan(data.loc[frame1, 'original_y'])):
        data.loc[frame1, 'original_y'] = -1
    frame2 = frame1 + 5
    x_coordinate = float(data.loc[frame1,'original_x'])
    x_coordinate2 = float(data.loc[frame2,'original_x'])
    y_coordinate = float(data.loc[frame1,'original_y'])
    y_coordinate2 = float(data.loc[frame2,'original_y'])
  
    #ans_idの判定
    if(0 <= x_coordinate2 <= 0.333):
        if(0 <= y_coordinate2 <= 0.333):
            ans_id = 1
        elif(0.333 < y_coordinate2 <= 0.666):
            ans_id = 4
        else:
            ans_id = 7
    elif(0.333 <= x_coordinate2 <= 0.666):
        if(0 <= y_coordinate2 <= 0.333):
            ans_id = 2
        elif(0.333 < y_coordinate2 <= 0.666):
            ans_id = 5
        else:
            ans_id = 8
    else:
        if(0 <= y_coordinate2 <= 0.333):
            ans_id = 3
        elif(0.333 < y_coordinate2 <= 0.666):
            ans_id = 6
        else:
            ans_id = 9
    stmt = f"UPDATE yolo_video_table SET frame1 = {frame1}, frame2 = {frame1 + 20}, ans_id = {ans_id}, x_coordinate = {x_coordinate}, y_coordinate = {y_coordinate}, yolo_flag = {2} WHERE video_path = '{fl}';"
    print(stmt)
    cur.execute(stmt)
    cur.close()
    conn.commit()
    conn.close()

    print('done!')
print('All completed!')