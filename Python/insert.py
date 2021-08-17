from decimal import Decimal
from re import T
from numpy.core.numeric import NaN
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pandas.io.json import json_normalize
import mysql.connector as mydb
import glob as gb
import math as m
import gc

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

folder = gb.glob("D:\\htdocs\\SEN-KEN\\2021SEN_KEN\\volleyball\\*\\*.json") #ローカル環境での実行用、運用時は消去

print(folder)

for lap,fl in enumerate(folder):
    # fl = fl.replace('IMG','ffmpeg')
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
    data['inped_ori_y'] = np.nan
    data['original_x'] = np.nan
    data['sabun_y'] = np.nan
    data['vertex_point'] = np.nan 
    data['ave_graph'] = np.nan 
    data['ave_graph2'] = np.nan 
    data['ave_graph3'] = np.nan 
    # data['low_area'] = np.nan
    # data['mid_area'] = np.nan
    # data['high_area'] = np.nan
    data['movave_5'] = np.nan   #差分を5で移動平均をとったものを格納する
    data['movave_40'] = np.nan  
    data['movave_50'] = np.nan  #差分を50で移動平均をとったものを格納する
    data['trend'] = np.nan
    data['panda_mov5'] = np.nan 
    data['panda_mov50'] = np.nan

    y_points = []
    hit_points = []
    mes_list = []       #ボールの上がり始めたフレームと少し下がり始めるまでフレームを格納するリストを格納するリスト
    mes_frame = []      #y座標の変位がマイナスからプラスになったフレームと、その次プラスからマイナスになったフレームを格納するリストを格納するリスト
    coor_list = []      #x,y座標のリストが格納されるリスト
    strange_list = []   #異常値の座標とその座標での検出回数のリストを格納するリスト
    ans = []            #プロット用変数
    vertex_point = []   #プロット用変数
    egg_frames = []     #プロット用変数
    intsec_inf = []     #5と50の移動平均のグラフの各交点のデータを格納するリスト
    intsec_max = []     #intsec_infの要素のリストの内一番多いintsec_cntを格納する物を格納するリスト

    nxt_val = 0         #
    obj_n = 0           #
    diff_tmp_x = 0      #
    diff_tmp_y = 0      #
    diff_tmp = 0        #
    stack = 0           #
    have_got = 0        #
    renzoku = 0         #
    phase = 0           #フラグ変数
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
        # print(i)
        obj_n = 0
        triple = '''{}'''.format(data.loc[i,'objects'])
        obj_list = eval(triple)
        # ---1フレームでオブジェクトが複数検出されていたなら座標を比べ適切な方を選択(機能していない)---
        if(obj_list):
            # print(obj_list)
            # for n,obj in enumerate(obj_list):
            #     diff_tmp_y = obj['relative_coordinates']['center_y'] - data.loc[i-stack,'center_y']
            #     diff_tmp_x = obj['relative_coordinates']['center_x'] - data.loc[i-stack,'center_x']
            #     if(diff_tmp > m.sqrt(diff_tmp_x**2 + diff_tmp_y**2) or n == 0):
            #         obj_n = n
            #     diff_tmp = m.sqrt(diff_tmp_x**2 + diff_tmp_y**2)
            #     y_points.append([i,obj['relative_coordinates']['center_y']])
            #     ans.append([i,obj_list[obj_n]['relative_coordinates']['center_y']])
            coor_list.append([obj_list[obj_n]['relative_coordinates']['center_y'],obj_list[obj_n]['relative_coordinates']['center_x']])
        else:
            coor_list.append([np.nan,np.nan])
            y_points.append([i,np.nan])

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

    data.loc[:,'inped_ori_y'] = data.loc[:,'original_y'].interpolate(axis=0)
    data.loc[:,'original_x'] = data.loc[:,'original_x'].interpolate(axis=0)

    #---グラフ出力、運用時はコメントアウト---
    # fig_list = [None,None,None,None]
    
    # fig_list[0] = plt.figure()
    # ax = fig_list[0].add_subplot(1,1,1)
    # data[:].plot('frame_id', 'inped_ori_y', c = 'black', zorder = 1, label = 'don\'t remove outliers', ax = ax)
    # for fy in y_points:
    #     plt.plot(fy[0], fy[1], c = 'red', zorder = 0, marker = '.', label = 'all objects', axes = ax)

    # fig_list[1] = plt.figure()
    # ax2 = fig_list[1].add_subplot(1,1,1)
    # data[:].plot('frame_id', 'inped_ori_y', c = 'black', zorder = 1, label = 'don\'t remove outliers', ax = ax2)
    # for fy in ans:
    #     plt.plot(fy[0], fy[1], c = 'red', zorder = 0, marker = '.', label = 'picked object', axes = ax2)

    # 異常値を弾く後前のグラフをプロット
    # fig_list[2] = plt.figure()
    # ax3 = fig_list[2].add_subplot(1,1,1)
    # data[:].plot('frame_id', 'center_y', c = 'red', zorder = 1, label = 'remove outliers', ax = ax3)
    # data[:].plot('frame_id', 'inped_ori_y', c = 'black', zorder = 0, label = 'don\'t remove outliers', ax = ax3)

    # fig_list[3] = plt.figure()
    # ax4 = fig_list[3].add_subplot(1,1,1)
    # data[:].plot('frame_id', 'center_y', c = 'red', zorder = 1, label = 'remove outliers', ax = ax4)

    # for i,fig in enumerate(fig_list, 1):
    #     ext = '.json'
    #     emp = ''
    #     fig.savefig(f'.\\graphs\\graph{emp.join(json_path.replace(ext,emp)[-4:])}_{i}.jpg')

    #溜まったfigure消化処理(プロット用)
    # if(lap == 50):
    #     plt.show()

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

        # # 前フレームとの差分を大きさによって三段階に分ける処理(プロット用)
        # if(abs(diff_y) < 0.001):
        #     data.loc[i,'low_area'] = data.loc[i,'center_y']
        # elif(0.001 <= abs(diff_y) and abs(diff_y) < 0.005):
        #     data.loc[i,'mid_area'] = data.loc[i,'center_y']
        # elif(0.005 <= abs(diff_y)):
        #     data.loc[i,'high_area'] = data.loc[i,'center_y']

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
                    hit_points.append([i - renzoku, data.loc[i - renzoku, 'center_y']])
                    renzoku = 0
                    phase = 2
                else:
                    renzoku = 0
                    # phase = 0
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

    # data['movave_5'] = data['sabun_y'].rolling(5, center=True).median()
    # data['movave_40'] = data['sabun_y'].rolling(40, center=True).median()
    # data['movave_50'] = data['sabun_y'].rolling(50, center=True).median()
    # for fr in range(0,len(data) - 1):
    #     data.loc[fr,'trend'] = (data.loc[fr,'movave_5'] + data.loc[fr,'movave_40'] + data.loc[fr,'movave_50'])/3

    # print(mes_list)
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
    # print(data['panda_mov5'].rolling(5, center=True))
    data['panda_mov5'] = data['panda_mov5'].rolling(5, center=False).mean()
    data['panda_mov50'] = data['panda_mov50'].rolling(50, center=False).mean()

    # #差分の5と50の移動平均をプロット
    # movave = plt.figure()
    # movaves = movave.add_subplot(1,1,1)
    # data[:].plot('frame_id', 'panda_mov5', c = 'black', ax = movaves)
    # data[:].plot('frame_id', 'panda_mov50', c = 'red', ax = movaves)
    # # data[:].plot('frame_id', 'sabun_y', c = 'blue', ax = movaves)
    
    # ---選択したフレームの間から5と50の差分の移動平均の差が広がったフレームを選択---
    egg_frames = []
    if(mes_frame):
        for m_frame in range(mes_frame[0], mes_frame[1]):
            if(data.loc[m_frame, 'panda_mov50'] - data.loc[m_frame, 'panda_mov5'] >= 0.002):
                frame1 = m_frame
                egg_frames.append(frame1) #egg_framesが元々frame1の候補が入るリストだった名残、実際は値は一つしか入らない
                break
            # print(m_frame, data.loc[m_frame, 'panda_mov50'] - data.loc[m_frame, 'panda_mov5'])
        # # プロット処理
        # for egg in egg_frames:
        #     plt.plot(egg, data.loc[egg,'panda_mov50'], c = 'blue', marker = '.', axes = movaves)

    # ---選択したフレームから遡り、5と50の移動平均の交点を見つける---
    if(mes_frame):
        for m_frame in range(frame1 - 1, mes_frame[0], -1):
            if(data.loc[m_frame, 'panda_mov5'] - data.loc[m_frame + 1, 'panda_mov5'] > 0):
                if((data.loc[m_frame, 'panda_mov50'] <= data.loc[m_frame, 'panda_mov5'] and data.loc[m_frame + 1, 'panda_mov5'] <= data.loc[m_frame + 1, 'panda_mov50']) or (data.loc[m_frame, 'panda_mov5'] <= data.loc[m_frame , 'panda_mov50'] and data.loc[m_frame + 1, 'panda_mov50'] <= data.loc[m_frame + 1, 'panda_mov5'])):
                    intsec_frame = m_frame + 1
                    frame1 = intsec_frame
                    # # プロット処理
                    # plt.plot(intsec_frame + 1, data.loc[intsec_frame, 'panda_mov5'], c = '#89f', marker = '.', axes = movaves)                    
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

    # data.loc[frame1-1,'vertex_point'] = data.loc[frame1-1, 'sabun_y']
    # data.loc[frame1,'vertex_point'] = data.loc[frame1, 'sabun_y']
    # data.loc[frame1+1,'vertex_point'] = data.loc[frame1+1, 'sabun_y']
    # sabun_fig = plt.figure()
    # sabun_ax = sabun_fig.add_subplot(1,1,1)
    # data[:].plot('frame_id', 'sabun_y', c = 'red', ax = sabun_ax)
    # data[:].plot('frame_id', 'vertex_point', c = 'black', ax = sabun_ax)

    # #y座標の変位のグラフにframe1などをプロット
    # y_coor = plt.figure()
    # ax_y = y_coor.add_subplot(1,1,1)
    # data.plot('frame_id', 'center_y', ax=ax_y)
    # plt.plot(frame1, data.loc[frame1, 'center_y'], marker='.', axes=ax_y)

    # data.loc[:,'vertex_point'] = np.nan
    # if(frame1 != 0):
    #     data.loc[frame1-1,'vertex_point'] = data.loc[frame1-1, 'center_y']
    #     vertex_point.append(frame1)
    #     vertex_point.append(data.loc[frame1,'center_y'])
    # data.loc[frame1,'vertex_point'] = data.loc[frame1, 'center_y']
    # data.loc[frame1+1,'vertex_point'] = data.loc[frame1+1, 'center_y']
    # data[:].plot('frame_id', 'center_y', c = 'red', zorder = 1, label = 'remove outliers', ax = ax_y)    
    # data[:].plot('frame_id', 'vertex_point', c = 'black', ax = ax_y)
    # if(vertex_point):
    #     plt.plot(vertex_point[0], vertex_point[1], c = 'blue', zorder = 2, marker = '.', label = 'all objects', axes = ax_y)
    # for hit in hit_points:
    #     plt.plot(hit[0], hit[1], c = 'black', marker = '.', label = 'all objects', axes = ax_y)
    # for egg in egg_frames:
    #     plt.plot(egg, data.loc[egg,'center_y'], c = 'blue', marker = '.', axes = ax_y)
    # plt.plot(intsec_frame + 1, data.loc[intsec_frame, 'center_y'], c = '#89f', marker = '.', axes = ax_y)

    #  area = plt.figure()
    # ax_area = area.add_subplot(1,1,1)
    # data[:].plot('frame_id', 'low_area', c = 'black', ax = ax_area)
    # data[:].plot('frame_id', 'mid_area', c = 'blue', ax = ax_area)
    # data[:].plot('frame_id', 'high_area', c = 'red', ax = ax_area)
    
    # ave = plt.figure()
    # aves = ave.add_subplot(1,1,1)
    # data.plot('frame_id', 'panda_mov5', c='red', ax=aves)
    # # data[:].plot('frame_id', 'movave_40', c = 'blue', ax = aves)
    # data.plot('frame_id', 'panda_mov50', c='black', ax=aves)
    # aves.axvline(frame1, c='#89d')
    # trend_fig = plt.figure()
    # trend = trend_fig.add_subplot(1,1,1)
    # data[:].plot('frame_id', 'trend', c = '#89e' , ax = trend)

    # plt.show()
    # movave.savefig(f'.\\graphs\\movave\\graph_{i}.jpg')
    # y_coor.savefig(f'.\\graphs\\center_y\\graph_{i}.jpg')

    # print(mes_frame)
    # print(mes_list)

    #---こっからDB関連---

    # コネクションの作成
    conn = mydb.connect(host='localhost',port='3306',user='root',password='',database='SEN-KEN')

    fl = fl.replace("\\", "/")
    # DB操作用にカーソルを作成
    cur = conn.cursor(buffered=True)
    fl = fl.replace(".json", ".MOV")
    fl = fl.replace("ffmpeg", "IMG")
    fl = fl.replace("D:/htdocs/", "../")
    # print(fl)
    
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

    # print(y_coordinate)
    # print(y_coordinate2)
  
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
    stmt = f"UPDATE yolo_video_table SET frame1 = {frame1}, frame2 = {frame2}, ans_id = {ans_id}, x_coordinate = {x_coordinate}, y_coordinate = {y_coordinate}, yolo_flag = {2} WHERE video_path = '{fl}';"
    # print(stmt)
    cur.execute(stmt)
    cur.close()
    conn.commit()
    conn.close()

    print('done!')
print('All completed!')