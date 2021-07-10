from decimal import Decimal
from re import T
from numpy.core.numeric import NaN
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pyautogui as key
from pandas.io.json import json_normalize
import mysql.connector as mydb
import glob as gb
import math as m
import gc

ball_id = 1 # バレー:1 バド:2 テニス:3
player_id = 1 # DBを参照
#---DBからyolo_flagが1の動画のパスを取得---
conn = mydb.connect(host='localhost',port='3306',user='root',password='',database='SEN-KEN')
cur = conn.cursor(buffered=True)
cur.execute("SELECT video_path FROM yolo_video_table WHERE yolo_flag = 1")
rows = cur.fetchall()
folder = []
for row in rows:
    folder.append(row[0])
cur.close
conn.commit()
conn.close()

rep_chk = 0
folder = gb.glob("D:\\htdocs\\2021SEN_KEN\\volleyball\\*\\*.json") #ローカル環境での実行用、運用時は消去
print(folder)

for lap,fl in enumerate(folder):
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
    y_points = []
    black_list = []
    ans = []
    b_flag = 0
    b_count = 0
    obj_n = 0
    diff_tmp_x = 0
    diff_tmp_y = 0
    diff_tmp = 0
    stack = 0
    checker = 0
    chk_tmp_x = 0
    chk_tmp_y = 0
    have_got = 0
    sign = 0
    permit_lock = 0
    cnt = 0
    vartex_cnt = 0
    vartex_flag = 0
    v_frame = 0
    renzoku_p = 0
    renzoku_m = 0
    phase = 0
    frame1 = 0

    for i in range(1,len(data) - 1):
        obj_n = 0
        diff_temp = 0
        b_count = 0
        triple = '''{}'''.format(data.loc[i,'objects'])
        obj_list = eval(triple)
        # # ---複数オブジェクトから適切な座標を抽出、及び異常値検出---
        # print("-------------------------------")
        # print(data.loc[i-stack,'center_y'])
        # if(obj_list):
        #     print(obj_list[0]['relative_coordinates']['center_y'])
        #     print(data.loc[i-stack,'center_y'] - obj_list[0]['relative_coordinates']['center_y'])
        # else:
        #     print(None)
        #     print(None)
        # print("-------------------------------")

        for n,obj in enumerate(obj_list):
            # print(black_list,b_flag)
            for b_coor in black_list:
                if(((b_coor[0] + (b_coor[0]/20)) >= obj['relative_coordinates']['center_y']) and ((b_coor[0] - (b_coor[0]/20)) <= obj['relative_coordinates']['center_y']) and ((b_coor[1] + (b_coor[1]/20)) >= obj['relative_coordinates']['center_x']) and ((b_coor[1] - (b_coor[1]/20)) <= obj['relative_coordinates']['center_x'])):
                    b_flag = 1
                    b_count += 1
            if(b_flag):
                b_flag = 0
                continue
            diff_tmp_y = obj['relative_coordinates']['center_y'] - data.loc[i-stack,'center_y']
            diff_tmp_x = obj['relative_coordinates']['center_x'] - data.loc[i-stack,'center_x']
            if(diff_tmp > m.sqrt(diff_tmp_x**2 + diff_tmp_y**2) or n == b_count):
                obj_n = n
            diff_tmp = m.sqrt(diff_tmp_x**2 + diff_tmp_y**2)
            y_points.append([i,obj['relative_coordinates']['center_y']])
            ans.append([i,obj_list[obj_n]['relative_coordinates']['center_y']])
            # y_points.append([i,obj_list[obj_n]['relative_coordinates']['center_y']])
            # print(obj_n)

        # if obj_list:
        #     data.loc[i,'original_y'] = obj_list[obj_n]['relative_coordinates']['center_y']
        #     data.loc[i,'original_x'] = obj_list[obj_n]['relative_coordinates']['center_x']
        #     if(not(np.isnan(data.loc[i-stack,'center_y']))):
        #         if(-0.02*(int(stack > 2)+1) < data.loc[i-stack,'center_y'] - obj_list[obj_n]['relative_coordinates']['center_y'] and data.loc[i-stack,'center_y'] - obj_list[obj_n]['relative_coordinates']['center_y'] < 0.02*stack):
        #             data.loc[i,'center_y'] = obj_list[obj_n]['relative_coordinates']['center_y']
        #             data.loc[i,'center_x'] = obj_list[obj_n]['relative_coordinates']['center_x']
        #             stack = 1
        #             cnt += 1
        #             # print(f"data.loc[{i-stack},'center_y'] is enable!")
        #         else:
        #             stack += 1
        #             # print(f"Displacement is too big so data.loc[{i},'center_y'] is disabled.")
        #     else:
        #         data.loc[i,'center_y'] = obj_list[obj_n]['relative_coordinates']['center_y']
        #         data.loc[i,'center_x'] = obj_list[obj_n]['relative_coordinates']['center_x']
        #         stack += 1
        #         # print(f"data.loc[{i-stack},'center_y'] is disable!")
        # else:
        #     stack += 1
        #     # print('no object!')
        if obj_list:
            data.loc[i,'original_y'] = obj_list[obj_n]['relative_coordinates']['center_y']
            data.loc[i,'original_x'] = obj_list[obj_n]['relative_coordinates']['center_x']
            if(not(np.isnan(data.loc[i-stack,'center_y'])) or not(have_got)):
                if(permit_lock and (sign*(obj_list[obj_n]['relative_coordinates']['center_y'] - data.loc[i - 1,'center_y']) > 0)):
                    data.loc[i,'center_y'] = obj_list[obj_n]['relative_coordinates']['center_y']
                    data.loc[i,'center_x'] = obj_list[obj_n]['relative_coordinates']['center_x']
                    print('permit mode!')
                else:
                    sign = 0
                    permit_lock = 0
                    if(-0.01 < data.loc[i-stack,'center_y'] - obj_list[obj_n]['relative_coordinates']['center_y'] and data.loc[i-stack,'center_y'] - obj_list[obj_n]['relative_coordinates']['center_y'] < 0.01 or not(have_got)):
                        data.loc[i,'center_y'] = obj_list[obj_n]['relative_coordinates']['center_y']
                        data.loc[i,'center_x'] = obj_list[obj_n]['relative_coordinates']['center_x']
                        have_got = 1
                        stack = 1
                        print(f"data.loc[{i-stack},'center_y'] in +-0.1")
                    else:
                        if(checker):
                            if((-0.0001 < obj_list[obj_n]['relative_coordinates']['center_y'] - chk_tmp_y and obj_list[obj_n]['relative_coordinates']['center_y'] - chk_tmp_y < 0.0001) or (sign*(obj_list[obj_n]['relative_coordinates']['center_y'] - chk_tmp_y) > 0)):
                                black_list.append([obj['relative_coordinates']['center_y'],obj['relative_coordinates']['center_x']])
                                stack += 1
                                checker = 0
                                print(f"[{obj['relative_coordinates']['center_y']},{obj['relative_coordinates']['center_x']}] was appended to black_list!")
                            else:
                                data.loc[i - 1,'center_y'] = chk_tmp_y
                                data.loc[i - 1,'center_x'] = chk_tmp_x
                                data.loc[i,'center_y'] = obj_list[obj_n]['relative_coordinates']['center_y']
                                data.loc[i,'center_x'] = obj_list[obj_n]['relative_coordinates']['center_x']
                                checker = 0
                                stack = 1
                                permit_lock = 1
                                print('permit mode on!')
                        else:
                            chk_tmp_x = obj_list[obj_n]['relative_coordinates']['center_x']
                            chk_tmp_y = obj_list[obj_n]['relative_coordinates']['center_y']
                            checker = 1
                            if(obj_list[obj_n]['relative_coordinates']['center_y'] - data.loc[i - stack,'center_y'] >= 0):
                                sign = 1
                            else:
                                sign = -1
                            stack += 1
                            print('checker turn on with sign:' + str(sign))
        else:
            if(have_got):
                stack += 1
            print('no object!')
        print(stack,have_got,checker,permit_lock,sign)

    data.loc[:,['center_y']] = data.loc[:,['center_y']].interpolate(axis=0)
    data.loc[:,['center_x']] = data.loc[:,['center_x']].interpolate(axis=0)
    data.loc[:,['original_y']] = data.loc[:,['original_y']].interpolate(axis=0)
    data.loc[:,['original_x']] = data.loc[:,['original_x']].interpolate(axis=0)

    #---グラフ出力、運用時はコメントアウト---
    fig_list = [None,None,None,None]
    
    fig_list[0] = plt.figure()
    ax = fig_list[0].add_subplot(1,1,1)
    data[:].plot('frame_id', 'original_y', c = 'black', zorder = 1, label = 'don\'t remove outliers', ax = ax)
    for fy in y_points:
        plt.plot(fy[0], fy[1], c = 'red', zorder = 0, marker = '.', label = 'all objects', axes = ax)

    fig_list[1] = plt.figure()
    ax2 = fig_list[1].add_subplot(1,1,1)
    data[:].plot('frame_id', 'original_y', c = 'black', zorder = 1, label = 'don\'t remove outliers', ax = ax2)
    for fy in ans:
        plt.plot(fy[0], fy[1], c = 'red', zorder = 0, marker = '.', label = 'picked object', axes = ax2)

    fig_list[2] = plt.figure()
    ax3 = fig_list[2].add_subplot(1,1,1)
    data[:].plot('frame_id', 'center_y', c = 'red', zorder = 1, label = 'remove outliers', ax = ax3)
    data[:].plot('frame_id', 'original_y', c = 'black', zorder = 0, label = 'don\'t remove outliers', ax = ax3)

    fig_list[3] = plt.figure()
    ax4 = fig_list[3].add_subplot(1,1,1)
    data[:].plot('frame_id', 'center_y', c = 'red', zorder = 1, label = 'remove outliers', ax = ax4)

    for i,fig in enumerate(fig_list, 1):
        ext = '.json'
        emp = ''
        fig.savefig(f'.\\graphs\\graph{emp.join(json_path.replace(ext,emp)[-4:])}_{i}.jpg')
    if(lap == 50):
        plt.show()

    #---スパイク検出---
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

        # if(data.loc[i,'sabun_y'] > 0):
        #     renzoku += 1
        # elif(data.loc[i, 'sabun_y'] <= 0 and renzoku > 20):
        #     renzoku = 0
        #     vartex_cnt += 1
        #     if(vartex_cnt==4):
        #         frame1 = i
        #         data.loc[frame1-1:frame1+1,'vartex_point'] = data.loc[frame1, 'sabun_y']
        # else:
        #     renzoku = 0

        if(i >= len(data)/2):
            if(phase == 0):
                if(data.loc[i,'sabun_y'] < 0):
                    renzoku_m += 1
                elif(data.loc[i, 'sabun_y'] >= 0 and renzoku_m > 20):
                    renzoku_m = 0
                    phase = 1
                else:
                    renzoku_m = 0
            elif(phase == 1):
                if(data.loc[i,'sabun_y'] <= 0):
                    renzoku_m += 1
                elif(data.loc[i,'sabun_y'] > 0 and renzoku_m > 5):
                    if(data.loc[i - renzoku_m, 'center_y'] <= data.loc[v_frame,'center_y'] or frame1 == 0):
                        v_frame = i - renzoku_m
                        renzoku_m = 0
                        phase = 2
                    else:
                        renzoku_m = 0
                else:
                    phase = 0
            elif(phase == 2):
                if(data.loc[i,'sabun_y'] <= 0):
                    renzoku_m += 1
                if(data.loc[i,'sabun_y'] <= 0 and renzoku_m > 5):
                    frame1 = i - renzoku_m
                    renzoku_m = 0
                    phase = 0
        
        # print(phase,v_frame)
                    
        first_x = Decimal(str(data.loc[i,'MedFilTemp_x']))
        second_x = Decimal(str(data.loc[i + 1,'MedFilTemp_x']))
        diff_x = second_x - first_x
        data.loc[i,'sabun_x'] = float(diff_x)

    data.loc[frame1-1:frame1+1,'vartex_point'] = data.loc[frame1, 'sabun_y']
    sabun_fig = plt.figure()
    sabun_ax = sabun_fig.add_subplot(1,1,1)
    data[:].plot('frame_id', 'sabun_y', c = 'red', ax = sabun_ax)
    data[:].plot('frame_id', 'vartex_point', c = 'black', ax = sabun_ax)
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