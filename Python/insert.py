from decimal import Decimal
from re import T
from numpy.core.numeric import NaN
import pandas as pd
import numpy as np
from pandas.io.json import json_normalize
import mysql.connector as mydb

ball_id = 1 # バレー:1 バド:2 テニス:3
player_id = 1 # DBを参照
#===DBからyolo_flagが1の動画のパスを取得===
conn = mydb.connect(host='localhost',port='3306',user='root',password='',database='SEN-KEN')
cur = conn.cursor(buffered=True)
cur.execute("SELECT video_path FROM yolo_video_table WHERE yolo_flag = 1")
rows = cur.fetchall()
folder = [] #jsonファイルへのパスを格納するリスト
for row in rows:
    folder.append(row[0])
cur.close
conn.commit()
conn.close()

print(folder)

for lap,fl in enumerate(folder):
    fl = fl.replace('IMG','ffmpeg')
    fl = fl.replace('MOV','json')
    fl = fl.replace('../',"D:\\htdocs\\SEN-KEN\\")
    fl = fl.replace('/',"\\")

    print(fl + 'を処理中...')

    #===jsonファイルのバックスラッシュが一個なら二個に置き換える処理===
    rep_chk = 0  #前のループでバックスラッシュを検出したかどうかのフラグ

    #---jsonファイルの中身を、一文字ずつ要素に入れたリストに変換---
    with open(fl, encoding="utf-8") as f:
        data_lines = f.read()
    chr_list = list(data_lines)
    #---リストを走査しバックスラッシュを検出、置換する---
    for c in chr_list:
        if(rep_chk == 0 and c == "\\"):
            rep_chk = 1
        elif(rep_chk == 1):
            if(c != "\\"):
                data_lines = data_lines.replace("\\","\\\\")
                with open(fl, encoding="utf-8", mode="w") as f:
                    f.write(data_lines)
            break

    #===jsonからcsvに変換===
    json_path = fl #頂点を取得するjsonファイル
    csv_path = fl.replace('json','csv')

    #---変換したいJSONファイルを読み込む---
    df = pd.read_json(json_path)
    df.to_csv(csv_path, encoding='utf-8')

    data = pd.read_csv(csv_path)

    #===ファイル毎に初期化する変数を宣言===
    data['center_y'] = np.nan
    data['center_x'] = np.nan
    data['original_y'] = np.nan
    data['original_x'] = np.nan
    data['sabun_y'] = np.nan
    data['panda_mov5'] = np.nan 
    data['panda_mov50'] = np.nan

    mes_list = []       #ボールの上がり始めたフレームと少し下がり始めるまでフレームを格納するリストを格納するリスト
    mes_frame = []      #y座標の変位がマイナスからプラスになったフレームと、その次プラスからマイナスになったフレームを格納するリストを格納するリスト
    coor_list = []      #x,y座標のリストが格納されるリスト
    strange_list = []   #異常値の座標とその座標での検出回数のリストを格納するリスト

    nxt_val = 0         #あるフレームの次のフレームの座標を格納する変数
    stack = 0           #最後に値が入っていたフレームを格納する変数
    have_got = 0        #各フレームの座標を精査していく際、もう値を取得したかのフラグ変数
    renzoku = 0         #ある条件に適する値が連続した回数を格納する変数
    phase = 0           #検出の段階を管理するフラグ変数
    frame1 = 0          #スパイクのフレーム
    frame2 = 0          #答え合わせを行うフレーム
    exist_cnt = 0       #frame2を検出する際に値が存在するフレームが連続した回数を保存する変数
    exist_frame = 0     #frame2を検出する際に最初に見つけた、値が存在するフレームを保存する変数
    intsec_frame = 0    #5と50ののグラフの交点のフレーム = frame1
    sample_frame = 0    #frame1が誤りであるかを判断するための試料となるフレームの範囲を格納する変数
    wrong_cnt = 0       #差分の変化が十分大きかった回数を格納する変数
    is_wrong = 0        #frame1が誤りであるかについてのフラグ変数
    wrong_frame = 0     #frame1が誤りであった場合にframe1を格納する変数
    loop_cnt = 0        #再検出を繰り返した回数を格納する変数
    big_diff_frame = 0  #差分の、5と50の移動平均の差が開いたフレームを格納する変数

    # ===csvファイルから各フレームごとのデータを取り出す===
    for i in range(0,len(data)):
        obj_n = 0
        triple = '''{}'''.format(data.loc[i,'objects'])
        obj_list = eval(triple)
        if(obj_list):
            coor_list.append([obj_list[obj_n]['relative_coordinates']['center_y'],obj_list[obj_n]['relative_coordinates']['center_x']])
        else:
            coor_list.append([np.nan,np.nan])

    # ===取り出したデータから異常値を省く===
    # ---異常値の候補をリストに格納---
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
                    # print(f"data.loc[{f},'center_y'] in +-0.01")
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
                                # print(f"[{coor_list[f][0]},{coor_list[f][1]}] was appended to strange_list!(frame = {f}),near:{(-0.003 < coor_list[f][0] - coor_list[nxt_val][0] and coor_list[f][0] - coor_list[nxt_val][0] < 0.003)},near_val:{coor_list[f][0] - coor_list[nxt_val][0]},now_val:{coor_list[f][0]},next_val:{coor_list[nxt_val][0]}")
                        if not(strange_list):
                            strange_list.append([coor_list[f][0],coor_list[f][1],0])
                            # print(f"[{coor_list[f][0]},{coor_list[f][1]}] was appended to strange_list!(frame = {f}),near:{(-0.003 < coor_list[f][0] - coor_list[nxt_val][0] and coor_list[f][0] - coor_list[nxt_val][0] < 0.003)},near_val:{coor_list[f][0] - coor_list[nxt_val][0]},now_val:{coor_list[f][0]},next_val:{coor_list[nxt_val][0]}")
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
                        # print(f"[{coor_list[f][0]},{coor_list[f][1]}] was appended to strange_list!(frame = {f}),vector:{(coor_list[stack][0] - coor_list[f][0])*(coor_list[f][0] - coor_list[nxt_val][0]) < 0},vector_val:{(coor_list[stack][0] - coor_list[f][0])*(coor_list[f][0] - coor_list[nxt_val][0])},now_val:{coor_list[f][0]},next_val{coor_list[nxt_val][0]}")
                    else:
                        data.loc[f,'center_y'] = coor_list[f][0]
                        data.loc[f,'center_x'] = coor_list[f][1]
                        stack = f
                        # print('passed check! near:' + str(coor_list[f][0] - coor_list[nxt_val][0]) + ',vector:' + str(Decimal(str(coor_list[stack][0] - coor_list[f][0]))*(Decimal(str(coor_list[f][0])) - Decimal(str(coor_list[nxt_val][0])))))
        else:
            # print('no object!')
            pass

    # ---異常値の候補から異常値を判断し空白に置換---
    # print(strange_list)
    for coor in strange_list:
        for i in range(0,len(data)):
            if(coor[0] - 0.001 <= data.loc[i,'center_y'] and data.loc[i,'center_y'] <= coor[0] + 0.001 and coor[2] >= 4):
                # print('deleted(frame:' + str(i) + ',y:' + str(data.loc[i,'center_y']) + ',x:' + str(data.loc[i,'center_x']) + ')')
                data.loc[i,'center_y'] = np.nan
                data.loc[i,'center_x'] = np.nan

    # ===データの空白を補完===
    data.loc[:,'center_y'] = data.loc[:,'center_y'].interpolate(axis=0)
    data.loc[:,'center_x'] = data.loc[:,'center_x'].interpolate(axis=0)

    data.loc[:,'original_y'] = data.loc[:,'original_y'].interpolate(axis=0)
    data.loc[:,'original_x'] = data.loc[:,'original_x'].interpolate(axis=0)

    # ===スパイク検出===
    # ---平滑化---
    data['MedFilTemp_y'] = data['center_y'].rolling(24, center=True).median()
    data.loc[:,'MedFilTemp_y'] = data.loc[:,['MedFilTemp_y']].interpolate(axis=0,limit_direction='both')
    data['MedFilTemp_x'] = data['center_x'].rolling(24, center=True).median()
    data.loc[:,'MedFilTemp_x'] = data.loc[:,['MedFilTemp_x']].interpolate(axis=0,limit_direction='both')  
    for i in range(0,len(data) - 1):
        # ---平滑化した値から差分をとる---
        first_y = Decimal(str(data.loc[i,'MedFilTemp_y']))
        second_y = Decimal(str(data.loc[i + 1,'MedFilTemp_y']))
        first_x = Decimal(str(data.loc[i,'MedFilTemp_x']))
        second_x = Decimal(str(data.loc[i + 1,'MedFilTemp_x']))
        diff_y = second_y - first_y
        diff_x = second_x - first_x
        data.loc[i,'sabun_y'] = float(diff_y)
        data.loc[i,'sabun_x'] = float(diff_x)

        # ---差分をもとにボールの上がり始めたフレームと少し下がり始めるまでフレームのリストをリストに格納---
        if(i >= (len(data)*1)/5):
            if(phase == 0):
                if(data.loc[i,'sabun_y'] < 0):
                    renzoku += 1
                elif(data.loc[i, 'sabun_y'] >= 0 and renzoku > 20):
                    renzoku = 0
                    phase = 1
                else:
                    renzoku = 0
            elif(phase == 1):
                if(data.loc[i,'sabun_y'] > 0 and renzoku <= 5):
                    renzoku += 1
                elif(data.loc[i,'sabun_y'] > 0 and renzoku > 5):
                    renzoku = 0
                    phase = 2
                else:
                    renzoku = 0
            elif(phase == 2):
                renzoku += 1
                if(renzoku <= 4):
                    pass
                elif(data.loc[i,'sabun_y'] >= -0.0005):
                    if(len(mes_list) == 0):
                        mes_list.append([i - renzoku])
                    elif(mes_list[-1][0] != i - renzoku):
                        mes_list.append([i - renzoku])
                else:
                    renzoku = 0
                    phase = 0
                    mes_list[-1].append(i)
                    
        if(mes_list):
            if(i == len(data) - 2 and len(mes_list[-1]) == 1):
                mes_list[-1].append(i)

    # ---リストに格納されているリストからスパイクが含まれるフレームと思われるものを選択---
    if(mes_list):
        if(len(mes_list) == 1):
            mes_frame = mes_list[0]
        elif(len(mes_list) == 2):
            mes_frame = mes_list[data.loc[mes_list[0][0], 'center_y'] > data.loc[mes_list[1][0], 'center_y']]
        else:
            mes_frame = mes_list[1]

    # ---差分の移動平均をとる---
    data.loc[:, 'panda_mov5'] = data.loc[:, 'sabun_y']
    data.loc[:, 'panda_mov50'] = data.loc[:, 'sabun_y']
    data['panda_mov5'] = data['panda_mov5'].rolling(5, center=False).mean()
    data['panda_mov50'] = data['panda_mov50'].rolling(50, center=False).mean()
    
    # ---選択したフレームの間から5と50の差分の移動平均の差が広がったフレームを選択---
    if(mes_frame):
        for m_frame in range(mes_frame[0], mes_frame[1]):
            if(data.loc[m_frame, 'panda_mov50'] - data.loc[m_frame, 'panda_mov5'] >= 0.002):
                big_diff_frame = m_frame
                break

    # ---選択したフレームから遡り、5と50の移動平均の交点を見つける---
    if(mes_frame):
        for m_frame in range(big_diff_frame - 1, mes_frame[0], -1):
            if(data.loc[m_frame, 'panda_mov5'] - data.loc[m_frame + 1, 'panda_mov5'] > 0):
                if((data.loc[m_frame, 'panda_mov50'] <= data.loc[m_frame, 'panda_mov5'] and data.loc[m_frame + 1, 'panda_mov5'] <= data.loc[m_frame + 1, 'panda_mov50']) or (data.loc[m_frame, 'panda_mov5'] <= data.loc[m_frame , 'panda_mov50'] and data.loc[m_frame + 1, 'panda_mov50'] <= data.loc[m_frame + 1, 'panda_mov5'])):
                    intsec_frame = m_frame + 1
                    frame1 = intsec_frame                 
                    break

    # ===取得したframe1が誤りでないか確認、誤りの場合しきい値を緩くして再検出===
    # ---frame1が誤りであるかを判断---
    if(frame1 + 30 > len(data) - 1):
        sample_frame = len(data) - 1
    else:
        sample_frame = frame1 + 30

    for fra in range(frame1 + 1, sample_frame, 1):
        if(-0.000001 < data.loc[fra, 'sabun_y'] - data.loc[fra - 1, 'sabun_y'] and data.loc[fra, 'sabun_y'] - data.loc[fra - 1, 'sabun_y'] < 0.000001):
            # print(fra - frame1, data.loc[fra, 'sabun_y'] - data.loc[fra - 1, 'sabun_y'])
            pass
        else:
            # print(data.loc[fra, 'sabun_y'] - data.loc[fra - 1, 'sabun_y'])
            wrong_cnt += 1
    
    if(wrong_cnt <= 3):
        is_wrong = 1
        wrong_frame = frame1
    else:
        is_wrong = 0
        wrong_frame = frame1

    # ---frame1を再検出---
    if(mes_frame):
        while(is_wrong):
            loop_cnt += 1
            for m_frame in range(mes_frame[0], mes_frame[1]):
                if(data.loc[m_frame, 'panda_mov50'] - data.loc[m_frame, 'panda_mov5'] >= 0.002 - (0.00001*loop_cnt)):
                    big_diff_frame = m_frame
                    break
            for m_frame in range(big_diff_frame - 1, mes_frame[0], -1):
                if(data.loc[m_frame, 'panda_mov5'] - data.loc[m_frame + 1, 'panda_mov5'] > 0):
                    if((data.loc[m_frame, 'panda_mov50'] <= data.loc[m_frame, 'panda_mov5'] and data.loc[m_frame + 1, 'panda_mov5'] <= data.loc[m_frame + 1, 'panda_mov50']) or (data.loc[m_frame, 'panda_mov5'] <= data.loc[m_frame , 'panda_mov50'] and data.loc[m_frame + 1, 'panda_mov50'] <= data.loc[m_frame + 1, 'panda_mov5'])):
                        intsec_frame = m_frame + 1
                        frame1 = intsec_frame
                        break
            if(frame1 != wrong_frame or 0.002 - (0.00001*loop_cnt) == 0):
                # print(loop_cnt)
                is_wrong = 0
    
    # ===frame2取得===
    for i in range(len(data) - 1,0,-1):
        if not(np.isnan(data.loc[i,'original_y'])):
            exist_cnt += 1
            if(exist_cnt == 1):
                exist_frame = i
            elif(exist_cnt == 3):
                frame2 = exist_frame - 4
                # print(frame2)
                break
        else:
            exist_cnt = 0
            exist_frame = 0
    if(frame2 <= frame1):
        frame2 = frame1 + 1

    # ===original_y,xのframe1,2が欠損値ならばcenter_y,xを適用する===
    if(np.isnan(data.loc[frame1, 'original_x'])):
        x_coordinate = data.loc[frame1, 'center_x']
    else:
        x_coordinate = data.loc[frame1, 'original_x']

    if(np.isnan(data.loc[frame2, 'original_x'])):
        x_coordinate2 = data.loc[frame2, 'center_x']
    else:
        x_coordinate2 = data.loc[frame2, 'original_x']

    if(np.isnan(data.loc[frame1, 'original_y'])):
        y_coordinate = data.loc[frame1, 'center_y']
    else:
        y_coordinate = data.loc[frame1, 'original_y']

    if(np.isnan(data.loc[frame2, 'original_y'])):
        y_coordinate2 = data.loc[frame2, 'center_y']
    else:
        y_coordinate2 = data.loc[frame2, 'original_y']
  
    # ===ans_idの判定===
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

    # ===DBに送信===
    if(not(np.isnan(x_coordinate) or np.isnan(y_coordinate))):
        # ---コネクションの作成---
        conn = mydb.connect(host='localhost',port='3306',user='root',password='',database='SEN-KEN')
        # ---DB操作用にカーソルを作成---
        cur = conn.cursor(buffered=True)
        # ---DBに送信するパスを生成---
        fl = fl.replace("\\", "/")
        fl = fl.replace(".json", ".MOV")
        fl = fl.replace("ffmpeg", "IMG")
        fl = fl.replace("D:/htdocs/SEN-KEN/", "../")
        # ----sql文を作成、実行--
        stmt = f"UPDATE yolo_video_table SET frame1 = {frame1}, frame2 = {frame2}, ans_id = {ans_id}, x_coordinate = {x_coordinate}, y_coordinate = {y_coordinate}, yolo_flag = {2} WHERE video_path = '{fl}';"
        cur.execute(stmt)
        # ---通信終了---
        cur.close()
        conn.commit()
        conn.close()

    print('done!')
print('All completed!')