#import json as j
from decimal import Decimal
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pandas.io.json import json_normalize
import mysql.connector as mydb
import glob as gb

ball_id = 1 # バレー:1 バド:2 テニス:3
player_id = 1 # DBを参照
 
folder = gb.glob("./graphs/*.json")
rep_chk = 0

for file in folder:
    print(file + 'を処理中...')
    with open(file, encoding="utf-8") as f:
        data_lines = f.read()
    chr_list = list(data_lines)
    for c in chr_list:
        if(rep_chk == 0 and c == "\\"):
            rep_chk = 1
        elif(rep_chk == 1):
            if(c != "\\"):
                data_lines = data_lines.replace("\\","\\\\")
                with open(file, encoding="utf-8", mode="w") as f:
                    f.write(data_lines)
            break

    rep_chk = 0
    json_path = file #頂点を取得するjsonファイル
    csv_path = file.replace('json','csv')

    #変換したいJSONファイルを読み込む
    df = pd.read_json(json_path)
    df.to_csv(csv_path, encoding='utf-8')

    data = pd.read_csv(csv_path)

    data['center_y'] = np.nan
    data['center_x'] = np.nan
    data['sabun_y'] = np.nan
    data['vartex_point'] = np.nan
    cnt = 0
    vartex_cnt = 0
    renzoku = 0
    frame1 = 0
    Zlist = []

    for i in range(0,len(data) - 1):
        triple = '''{}'''.format(data.loc[i,'objects'])
        obj_list = eval(triple)
        if obj_list:
            data.loc[i,'center_y'] = obj_list[0]['relative_coordinates']['center_y']
            data.loc[i,'center_x'] = obj_list[0]['relative_coordinates']['center_x']

    data.loc[:,['center_y']] = data.loc[:,['center_y']].interpolate(axis=0)
    data.loc[:,['center_x']] = data.loc[:,['center_x']].interpolate(axis=0)

    data['MedFilTemp_y'] = data['center_y'].rolling(24, center=True).median()
    data.loc[:,'MedFilTemp_y'] = data.loc[:,['MedFilTemp_y']].interpolate(axis=0,limit_direction='both')
    data['MedFilTemp_x'] = data['center_x'].rolling(24, center=True).median()
    data.loc[:,'MedFilTemp_x'] = data.loc[:,['MedFilTemp_x']].interpolate(axis=0,limit_direction='both')

    for i in range(1,len(data) - 1):
        
        first_y = Decimal(str(data.loc[i,'MedFilTemp_y']))
        second_y = Decimal(str(data.loc[i + 1,'MedFilTemp_y']))
        diff_y = second_y - first_y

        # if(diff_y > Decimal('0')):
        #     diff_y = 1
        # elif(diff_y < Decimal('0')):
        #     diff_y = -1
        # elif(diff_y == Decimal('0')):
        #     diff_y = 0

        if(diff_y > Decimal('0.0075')):
            diff_y = 0.0075
        elif(diff_y < Decimal('-0.0075')):
            diff_y = -0.0075

        data.loc[i,'sabun_y'] = float(diff_y)
        
        if(data.loc[i,'sabun_y'] == 0):
            renzoku = 1
            cnt += 1
            Zlist.append(i)
        if((data.loc[i, 'sabun_y'] != 0 and renzoku != 0) or (i == len(data) - 2)):
            renzoku = 0
            if(cnt >= 4):
                vartex_cnt += 1
                if vartex_cnt == 9:
                    frame1 = Zlist[0]
                    for n in Zlist:
                        data.loc[n,'vartex_point'] = 0
            Zlist = []
            cnt = 0

        first_x = Decimal(str(data.loc[i,'MedFilTemp_x']))
        second_x = Decimal(str(data.loc[i + 1,'MedFilTemp_x']))
        diff_x = second_x - first_x
        data.loc[i,'sabun_x'] = float(diff_x)
        #print(i,data.loc[i,'sabun_x'])

    # for i in range(1,len(data) - 1):
    #     print(data.loc[i, 'vartex_point'])

    ax = data[:].plot('frame_id', 'sabun_y', c = 'red')
    #data[:].plot('frame_id', 'sabun_x', c = 'blue', ax = ax)
    data[:].plot('frame_id', 'vartex_point', c = 'black', ax = ax)
    #plt.show()

    #---こっからDB関連---

    # コネクションの作成
    conn = mydb.connect(host='localhost',port='3306',user='root',password='',database='hikaku_test_db')

    # コネクションが切れた時に再接続してくれるよう設定
    #conn.ping(reconnect=True)
    # 接続できているかどうか確認
    #print(conn.is_connected())

    # DB操作用にカーソルを作成
    cur = conn.cursor(buffered=True)

    cur.execute(cur.execute(f"UPDATE yolo_video_table SET frame1 = {frame1}, frame2 = {frame1 + 20}, x_coordinate = {data.loc[frame1,'center_x']}, y_coordinate = {data.loc[frame1,'center_y']}, yolo_flag = {1}"))

    cur.close()
    conn.commit()
    conn.close()

    print('done!')
print('All completed!')