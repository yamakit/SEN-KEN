from decimal import Decimal
from re import T
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pandas.io.json import json_normalize
import mysql.connector as mydb
import glob as gb
import math as m

ball_id = 2 # バレー:1 バド:2 テニス:3
player_id = 1 # DBを参照

conn = mydb.connect(host='localhost',port='3306',user='root',password='',database='SEN-KEN')
cur = conn.cursor(buffered=True)
cur.execute("SELECT video_path FROM yolo_video_table WHERE yolo_flag = 1 and ball_id = 2")
rows = cur.fetchall()
folder = []
for row in rows:
    folder.append(row[0])
cur.close
conn.commit()
conn.close()
rep_chk = 0

folder = gb.glob("D:\\htdocs\\2021SEN_KEN\\badminton\\1\\*.json") #ローカル環境での実行用、運用時は削除

for fl in folder:
    fl = fl.replace('IMG', 'ffmpeg')
    fl = fl.replace('MOV', 'json')
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
    data['original_y'] = np.nan
    data['center_y'] = np.nan
    data['center_x'] = np.nan
    data['sabun_y'] = np.nan
    data['sabun_x'] = np.nan
    data['vartex_point'] = np.nan

    cnt = 0
    vartex = 0
    renzoku = 0
    found = 0
    frame1 = 0
    aiuw = 0
    stack = 0
    diff_tmp = 0
    strange_flag = 0 #最初の2フレームが異常値かどうかの判定結果を格納する変数
    nan_flag = 0     #異常値だった場合にその値を空白にしたという処理をしたことを記録する変数

    Zlist = []
    y_points = []  #フレームとそのフレームのy座標を格納するリスト
    ans = []       #
    coor_list = [] #座標を格納するリスト
    strange_coor = [] #異常値の基準となる座標を格納するリスト

    #===csvから座標を取り出す===
    # #---慢性的に検出される異常値を検出---
    # obj1 = eval('''{}'''.format(data.loc[0, 'objects']))
    # obj2 = eval('''{}'''.format(data.loc[1, 'objects']))
    # if(obj1 and obj2):
    #     if(-0.004 < obj1[0]['relative_coordinates']['center_y'] - obj2[0]['relative_coordinates']['center_y'] and obj1[0]['relative_coordinates']['center_y'] - obj2[0]['relative_coordinates']['center_y'] < 0.004):
    #         if(-0.004 < obj1[0]['relative_coordinates']['center_x'] - obj2[0]['relative_coordinates']['center_x'] and obj1[0]['relative_coordinates']['center_x'] - obj2[0]['relative_coordinates']['center_x'] < 0.004):
    #             strange_coor = [obj1[0]['relative_coordinates']['center_y'],obj1[0]['relative_coordinates']['center_x']]
    #             strange_flag = 1
    # #---csvから慢性的に検出される異常値を弾いて座標を取り出す---
    # if(strange_flag):
    #     for i in range(0,len(data)):
    #         triple = '''{}'''.format(data.loc[i,'objects'])
    #         obj_list = eval(triple)
    #         coor_list.append([])
    #         if(obj_list):
    #             for n,obj in enumerate(obj_list):
    #                 if((-0.004 < obj['relative_coordinates']['center_y'] - strange_coor[0] and obj['relative_coordinates']['center_y'] - strange_coor[0] < 0.004) and (-0.004 < obj['relative_coordinates']['center_x'] - strange_coor[1] and obj['relative_coordinates']['center_x'] - strange_coor[1] < 0.004)):
    #                     pass
    #                 else:
    #                     coor_list[-1].append([obj['relative_coordinates']['center_y'],obj['relative_coordinates']['center_x']])
    # else:
    #     for i in range(0,len(data)):
    #         triple = '''{}'''.format(data.loc[i,'objects'])
    #         obj_list = eval(triple)
    #         coor_list.append([])
    #         if(obj_list):
    #             for n,obj in enumerate(obj_list):
    #                 coor_list[-1].append([obj['relative_coordinates']['center_y'],obj['relative_coordinates']['center_x']])
    # print(coor_list)

    # print(len(coor_list))
    # print([coor_list[aiuw][0] if coor_list[aiuw] else coor_list[aiuw] for aiuw in range(len(coor_list))])
    # plt.plot([coor_list[aiuw][0] if coor_list[aiuw] else coor_list[aiuw] for aiuw in range(len(coor_list))])
    # plt.show()
    # #---coor_listの中から適切な座標を取り出す---
    # for i in range(0,len(data)):
    #     obj_n = 0
    #     triple = '''{}'''.format(data.loc[i,'objects'])
    #     obj_list = eval(triple)
    #     # ---1フレームでオブジェクトが複数検出されていたなら座標を比べ適切な方を選択---
    #     if(obj_list):
    #         for n,obj in enumerate(obj_list):
    #             diff_tmp_y = obj['relative_coordinates']['center_y'] - data.loc[i,'center_y']
    #             diff_tmp_x = obj['relative_coordinates']['center_x'] - data.loc[i,'center_x']
    #             if(strange_flag):
    #                 if((-0.004 < obj['relative_coordinates']['center_y'] - strange_coor[0] and obj['relative_coordinates']['center_y'] - strange_coor[0] < 0.004) and (-0.004 < obj['relative_coordinates']['center_x'] - strange_coor[1] and obj['relative_coordinates']['center_x'] - strange_coor[1] < 0.004)):
    #                     if(n == len(obj_list) - 1):
    #                         coor_list.append([np.nan,np.nan])
    #                         nan_flag = 1
    #                     continue
    #             if(diff_tmp > m.sqrt(diff_tmp_x**2 + diff_tmp_y**2) or n == 0):
    #                 obj_n = n
    #             diff_tmp = m.sqrt(diff_tmp_x**2 + diff_tmp_y**2)
    #             y_points.append([i,obj['relative_coordinates']['center_y']])
    #             ans.append([i,obj_list[obj_n]['relative_coordinates']['center_y']])
    #         if(nan_flag == 0):
    #             coor_list.append([obj_list[obj_n]['relative_coordinates']['center_y'],obj_list[obj_n]['relative_coordinates']['center_x']])
    #         else:
    #             nan_flag = 0
    #     else:
    #         coor_list.append([np.nan,np.nan])
    #         y_points.append([i,np.nan])
    
    # 旧 データ取り出し処理
    for i in range(1,len(data) - 1):
        triple = '''{}'''.format(data.loc[i,'objects'])
        obj_list = eval(triple)
        if obj_list:
            data.loc[i,'center_y'] = obj_list[0]['relative_coordinates']['center_y']
            data.loc[i,'center_x'] = obj_list[0]['relative_coordinates']['center_x']
            data.loc[i,'original_y'] = obj_list[0]['relative_coordinates']['center_y']

    data.loc[:,['center_y']] = data.loc[:,['center_y']].interpolate(axis=0)
    data.loc[:,['center_x']] = data.loc[:,['center_x']].interpolate(axis=0)

    data['MedFilTemp_y'] = data['center_y'].rolling(24, center=True).median()
    data.loc[:,'MedFilTemp_y'] = data.loc[:,['MedFilTemp_y']].interpolate(axis=0,limit_direction='both')
    data['MedFilTemp_x'] = data['center_x'].rolling(24, center=True).median()
    data.loc[:,'MedFilTemp_x'] = data.loc[:,['MedFilTemp_x']].interpolate(axis=0,limit_direction='both')

    #===frame1検出===

    for i in range(1,len(data) - 1):
        
        first_y = Decimal(str(data.loc[i,'MedFilTemp_y']))
        second_y = Decimal(str(data.loc[i + 1,'MedFilTemp_y']))
        diff_y = second_y - first_y
        if(diff_y > Decimal('0.0075')):
            diff_y = 0.0075
        elif(diff_y < Decimal('-0.0075')):
            diff_y = -0.0075

        if(diff_y < Decimal('0.0001') and diff_y > Decimal('-0.0001')):
            diff_y = 0

        data.loc[i,'sabun_y'] = float(diff_y)

        # ------
        if(found == 0):
            if(data.loc[i,'sabun_y'] > 0):
                vartex = 0
                renzoku += 1
                cnt = 0
            if(data.loc[i, 'sabun_y'] == 0 and renzoku > 50):
                cnt = 0
                if(data.loc[i - 1,'sabun_y'] != 0):
                    vartex = 1
                    frame1 = i
            if(data.loc[i, 'sabun_y'] < 0 and vartex):
                if(cnt > 5):
                    renzoku = 0
                cnt += 1
                if(cnt > 10 and data.loc[i - 11, 'sabun_y'] == 0):
                    data.loc[frame1-1:frame1+1,'vartex_point'] = data.loc[frame1, 'sabun_y']
                    found = 1
            if(len(data) - 2 == i):
                data.loc[frame1-1:frame1+1,'vartex_point'] = data.loc[frame1, 'sabun_y']
                found = 1
        # ------

        first_x = Decimal(str(data.loc[i,'MedFilTemp_x']))
        second_x = Decimal(str(data.loc[i + 1,'MedFilTemp_x']))
        diff_x = second_x - first_x
        data.loc[i,'sabun_x'] = float(diff_x)

    oriY_fig = plt.figure()
    oriY_ax = oriY_fig.add_subplot(1,1,1)
    data[:].plot('frame_id', 'original_y', c = 'black', ax = oriY_ax)

    cenY_fig = plt.figure()
    cenY_ax = cenY_fig.add_subplot(1,1,1)
    data[:].plot('frame_id', 'center_y', c = 'black', ax = cenY_ax)
    
    sabY_fig = plt.figure()
    sabY_ax = sabY_fig.add_subplot(1,1,1)
    data[:].plot('frame_id', 'sabun_y', c = 'black', ax = sabY_ax)

    # plt.show()

    #---こっからDB関連---

    # コネクションの作成
    conn = mydb.connect(host='localhost',port='3306',user='root',password='',database='sen-ken')

    fl = fl.replace("\\", "/")
    # DB操作用にカーソルを作成
    cur = conn.cursor(buffered=True)
    fl = fl.replace(".json", ".MOV")
    fl = fl.replace("ffmpeg", "IMG")
    fl = fl.replace("D:/htdocs/", "../")
    # print(fl)
    if(np.isnan(data.loc[frame1, 'center_x'])):
        data.loc[frame1, 'center_x'] = -1
    if(np.isnan(data.loc[frame1, 'center_y'])):
        data.loc[frame1, 'center_y'] = -1
    frame2 = frame1 + 5
    x_coordinate = float(data.loc[frame1,'center_x'])
    x_coordinate2 = float(data.loc[frame2,'center_x'])
    y_coordinate = float(data.loc[frame1,'center_y'])
    y_coordinate2 = float(data.loc[frame2,'center_y'])
 
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

    # print(x_coordinate,y_coordinate)
    stmt = f"UPDATE yolo_video_table SET frame1 = {frame1}, frame2 = {frame1 + 20}, ans_id = {ans_id}, x_coordinate = {x_coordinate}, y_coordinate = {y_coordinate}, yolo_flag = 2 WHERE video_path = '{fl}';"
    cur.execute(stmt)
    cur.close()
    conn.commit()
    conn.close()

    print('done!')
print('All completed!')