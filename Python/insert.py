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
# folder = gb.glob("D:\\htdocs\\2021SEN_KEN\\volleyball\\*\\*.json") #ローカル環境での実行用、運用時は消去
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
    # data['low_area'] = np.nan
    # data['mid_area'] = np.nan
    # data['high_area'] = np.nan

    y_points = []
    coor_list = []
    strange_list = []
    ans = []
    nxt_val = 0
    obj_n = 0
    diff_tmp_x = 0
    diff_tmp_y = 0
    diff_tmp = 0
    stack = 0
    have_got = 0
    sign = 0
    v_frame = 0
    renzoku = 0
    phase = 0
    frame1 = 0

    for i in range(0,len(data)):
        obj_n = 0
        diff_temp = 0
        triple = '''{}'''.format(data.loc[i,'objects'])
        obj_list = eval(triple)
        # # ---複数オブジェクトから適切な座標を抽出---
        # print("-------------------------------")
        # print(data.loc[i-stack,'center_y'])
        # if(obj_list):
        #     print(obj_list[0]['relative_coordinates']['center_y'])
        #     print(data.loc[i-stack,'center_y'] - obj_list[0]['relative_coordinates']['center_y'])
        # else:
        #     print(None)
        #     print(None)
        # print("-------------------------------")
        if(obj_list):
            for n,obj in enumerate(obj_list):
                diff_tmp_y = obj['relative_coordinates']['center_y'] - data.loc[i-stack,'center_y']
                diff_tmp_x = obj['relative_coordinates']['center_x'] - data.loc[i-stack,'center_x']
                if(diff_tmp > m.sqrt(diff_tmp_x**2 + diff_tmp_y**2) or n == 0):
                    obj_n = n
                diff_tmp = m.sqrt(diff_tmp_x**2 + diff_tmp_y**2)
                y_points.append([i,obj['relative_coordinates']['center_y']])
                ans.append([i,obj_list[obj_n]['relative_coordinates']['center_y']])
            if(obj_list):
                coor_list.append([obj_list[obj_n]['relative_coordinates']['center_y'],obj_list[obj_n]['relative_coordinates']['center_x']])
            else:
                coor_list.append([np.nan,np.nan])
                y_points.append([i,obj_list[obj_n]['relative_coordinates']['center_y']])

    for f in range(0,len(coor_list)):
        data.loc[f,'original_y'] = coor_list[f][0]
        data.loc[f,'original_x'] = coor_list[f][1]
        if not(np.isnan(coor_list[f][0])):
            if not(have_got):
                data.loc[f,'center_y'] = coor_list[f][0]
                data.loc[f,'center_x'] = coor_list[f][1]
                have_got = 1
                stack = f
            else:
                if(-0.005 < coor_list[stack][0] - coor_list[f][0] and coor_list[stack][0] - coor_list[f][0] < 0.005 or not(have_got)):
                    data.loc[f,'center_y'] = coor_list[f][0]
                    data.loc[f,'center_x'] = coor_list[f][1]
                    stack = f
                    if(coor_list[stack][0] - coor_list[f][0] >= 0):
                        sign = -1
                    else:
                        sign = 1
                    print(f"data.loc[{f},'center_y'] in +-0.01")
                else:
                    for coor in range(f + 1,len(coor_list)):
                        if not(np.isnan(coor_list[coor][0])):
                            nxt_val = coor
                            break
                    if(-0.003 < coor_list[f][0] - coor_list[nxt_val][0] and coor_list[f][0] - coor_list[nxt_val][0] < 0.003):
                        for num,strange in enumerate(strange_list):
                            if(-0.001 <= strange[0] - coor_list[f][0] and strange[0] - coor_list[f][0] <= 0.001):
                                strange_list[num][2] += 1
                                break
                            if(num == len(strange_list) - 1):
                                strange_list.append([coor_list[f][0],coor_list[f][1],0])
                                print(f"[{coor_list[f][0]},{coor_list[f][1]}] was appended to strange_list!(frame = {f}),near:{(-0.003 < coor_list[f][0] - coor_list[nxt_val][0] and coor_list[f][0] - coor_list[nxt_val][0] < 0.003)},near_val:{coor_list[f][0] - coor_list[nxt_val][0]},now_val:{coor_list[f][0]},next_val:{coor_list[nxt_val][0]}")
                        if not(strange_list):
                            strange_list.append([coor_list[f][0],coor_list[f][1],0])
                            print(f"[{coor_list[f][0]},{coor_list[f][1]}] was appended to strange_list!(frame = {f}),near:{(-0.003 < coor_list[f][0] - coor_list[nxt_val][0] and coor_list[f][0] - coor_list[nxt_val][0] < 0.003)},near_val:{coor_list[f][0] - coor_list[nxt_val][0]},now_val:{coor_list[f][0]},next_val:{coor_list[nxt_val][0]}")
                        data.loc[f,'center_y'] = coor_list[f][0]
                        data.loc[f,'center_x'] = coor_list[f][1]
                    elif((coor_list[stack][0] - coor_list[f][0])*(coor_list[f][0] - coor_list[nxt_val][0]) < 0):
                        for num,strange in enumerate(strange_list):
                            if(-0.001 <= strange[0] - coor_list[f][0] and strange[0] - coor_list[f][0] <= 0.001):
                                strange_list[num][2] += 1
                                break
                            if(num == len(strange_list) + 1):
                                strange_list.append([coor_list[f][0],coor_list[f][1],0])
                        if not(strange_list):
                            strange_list.append([coor_list[f][0],coor_list[f][1],0])
                        print(f"[{coor_list[f][0]},{coor_list[f][1]}] was appended to strange_list!(frame = {f}),vector:{(coor_list[stack][0] - coor_list[f][0])*(coor_list[f][0] - coor_list[nxt_val][0]) < 0},vector_val:{(coor_list[stack][0] - coor_list[f][0])*(coor_list[f][0] - coor_list[nxt_val][0])},now_val:{coor_list[f][0]},next_val{coor_list[nxt_val][0]}")
                    else:
                        data.loc[f,'center_y'] = coor_list[f][0]
                        data.loc[f,'center_x'] = coor_list[f][1]
                        stack = f
                        print('passed check! near:' + str(coor_list[f][0] - coor_list[nxt_val][0]) + ',vector:' + str(Decimal(str(coor_list[stack][0] - coor_list[f][0]))*(Decimal(str(coor_list[f][0])) - Decimal(str(coor_list[nxt_val][0])))))
        else:
            print('no object!')

    print(strange_list)
    for coor in strange_list:
        for i in range(0,len(data)):
            if(coor[0] - 0.001 <= data.loc[i,'center_y'] and data.loc[i,'center_y'] <= coor[0] + 0.001 and coor[2] >= 4):
                print('deleted(frame:' + str(i) + ',y:' + str(data.loc[i,'center_y']) + ',x:' + str(data.loc[i,'center_x']) + ')')
                data.loc[i,'center_y'] = np.nan
                data.loc[i,'center_x'] = np.nan

    data.loc[:,['center_y']] = data.loc[:,['center_y']].interpolate(axis=0)
    data.loc[:,['center_x']] = data.loc[:,['center_x']].interpolate(axis=0)
    data.loc[:,['original_y']] = data.loc[:,['original_y']].interpolate(axis=0)
    data.loc[:,['original_x']] = data.loc[:,['original_x']].interpolate(axis=0)

    #---グラフ出力、運用時はコメントアウト---
    fig_list = [None,None,None,None]
    
    # fig_list[0] = plt.figure()
    # ax = fig_list[0].add_subplot(1,1,1)
    # data[:].plot('frame_id', 'original_y', c = 'black', zorder = 1, label = 'don\'t remove outliers', ax = ax)
    # for fy in y_points:
    #     plt.plot(fy[0], fy[1], c = 'red', zorder = 0, marker = '.', label = 'all objects', axes = ax)

    # fig_list[1] = plt.figure()
    # ax2 = fig_list[1].add_subplot(1,1,1)
    # data[:].plot('frame_id', 'original_y', c = 'black', zorder = 1, label = 'don\'t remove outliers', ax = ax2)
    # for fy in ans:
    #     plt.plot(fy[0], fy[1], c = 'red', zorder = 0, marker = '.', label = 'picked object', axes = ax2)

    # fig_list[2] = plt.figure()
    # ax3 = fig_list[2].add_subplot(1,1,1)
    # data[:].plot('frame_id', 'center_y', c = 'red', zorder = 1, label = 'remove outliers', ax = ax3)
    # data[:].plot('frame_id', 'original_y', c = 'black', zorder = 0, label = 'don\'t remove outliers', ax = ax3)

    # fig_list[3] = plt.figure()
    # ax4 = fig_list[3].add_subplot(1,1,1)
    # data[:].plot('frame_id', 'center_y', c = 'red', zorder = 1, label = 'remove outliers', ax = ax4)

    # for i,fig in enumerate(fig_list, 1):
    #     ext = '.json'
    #     emp = ''
    #     fig.savefig(f'.\\graphs\\graph{emp.join(json_path.replace(ext,emp)[-4:])}_{i}.jpg')

    # if(lap == 50):
    #     plt.show()

    #---スパイク検出---
    data['MedFilTemp_y'] = data['center_y'].rolling(24, center=True).median()
    data.loc[:,'MedFilTemp_y'] = data.loc[:,['MedFilTemp_y']].interpolate(axis=0,limit_direction='both')
    data['MedFilTemp_x'] = data['center_x'].rolling(24, center=True).median()
    data.loc[:,'MedFilTemp_x'] = data.loc[:,['MedFilTemp_x']].interpolate(axis=0,limit_direction='both')  
    for i in range(0,len(data) - 1):
        
        first_y = Decimal(str(data.loc[i,'MedFilTemp_y']))
        second_y = Decimal(str(data.loc[i + 1,'MedFilTemp_y']))
        diff_y = second_y - first_y

        data.loc[i,'sabun_y'] = float(diff_y)

        if(abs(diff_y) < 0.001):
            data.loc[i,'low_area'] = data.loc[i,'center_y']
        elif(0.001 <= abs(diff_y) and abs(diff_y) < 0.005):
            data.loc[i,'mid_area'] = data.loc[i,'center_y']
        elif(0.005 <= abs(diff_y)):
            data.loc[i,'high_area'] = data.loc[i,'center_y']

        if(i >= len(data)/2):
            if(phase == 0):
                if(data.loc[i,'sabun_y'] < 0):
                    renzoku += 1
                elif(data.loc[i, 'sabun_y'] >= 0 and renzoku > 20):
                    renzoku = 0
                    phase = 1
                else:
                    renzoku = 0
            elif(phase == 1):
                if(data.loc[i,'sabun_y'] <= 0):
                    renzoku += 1
                elif(data.loc[i,'sabun_y'] > 0 and renzoku > 5):
                    if(data.loc[i - renzoku, 'center_y'] <= data.loc[v_frame,'center_y'] or frame1 == 0):
                        v_frame = i - renzoku
                        renzoku = 0
                        phase = 2
                    else:
                        renzoku = 0
                else:
                    phase = 0
            elif(phase == 2):
                if(data.loc[i,'sabun_y'] <= 0):
                    renzoku += 1
                if(data.loc[i,'sabun_y'] <= 0 and renzoku > 5):
                    frame1 = i - renzoku
                    renzoku = 0
                    phase = 0
        
        # print(phase,v_frame)
                    
        first_x = Decimal(str(data.loc[i,'MedFilTemp_x']))
        second_x = Decimal(str(data.loc[i + 1,'MedFilTemp_x']))
        diff_x = second_x - first_x
        data.loc[i,'sabun_x'] = float(diff_x)

    # data.loc[frame1-1:frame1+1,'vartex_point'] = data.loc[frame1, 'sabun_y']
    # sabun_fig = plt.figure()
    # sabun_ax = sabun_fig.add_subplot(1,1,1)
    # data[:].plot('frame_id', 'sabun_y', c = 'red', ax = sabun_ax)
    # data[:].plot('frame_id', 'vartex_point', c = 'black', ax = sabun_ax)
    # y_coor = plt.figure()
    # ax_y = y_coor.add_subplot(1,1,1)
    # data.loc[:,'vartex_point'] = np.nan
    # data.loc[frame1-1:frame1+1,'vartex_point'] = data.loc[frame1, 'center_y']
    # data[:].plot('frame_id', 'center_y', c = 'red', zorder = 1, label = 'remove outliers', ax = ax_y)    
    # data[:].plot('frame_id', 'vartex_point', c = 'black', ax = ax_y)
    # area = plt.figure()
    # ax_area = area.add_subplot(1,1,1)
    # data[:].plot('frame_id', 'low_area', c = 'black', ax = ax_area)
    # data[:].plot('frame_id', 'mid_area', c = 'blue', ax = ax_area)
    # data[:].plot('frame_id', 'high_area', c = 'red', ax = ax_area)

    # plt.show()

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