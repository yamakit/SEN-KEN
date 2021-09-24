import pandas as pd
from pandas.io.json import json_normalize
import matplotlib.pyplot as plt
import json
import numpy as np
import glob as gb
import mysql.connector as mydb

# files = gb.glob('目的のファイルが入っているフォルダーへのパス\\*.xlsx') #運用時の処理
files = gb.glob('D:/htdocs/SEN-KEN/2021SEN_KEN/volleyball/03/*.csv')      #ローカル環境での実行用

#===データを取り出すjsonファイルが入っているフォルダー群を回す===
for file in files:
    move_list = []
    move_area = 5
    turning_body_list = []
    have_got = 0
    base_frame = 0
    checker = 0
    check_frame = 0
    
    #===フォルダーからcsvファイルを取り出す===
    print(f'{file}を処理')
    
    #===データ取り出し===
    df = pd.read_csv(file)              
    if(df.empty == False):

        #===データフレームを用意===
        body_columns = ['LNdis', 'NRdis', 'turning_face', 'turning_body', 'filterd_turning_body', 'filterd_REar_x']     #カラム名を用意
        df[body_columns] = np.nan                                                        #用意したカラム名の列を作成

        for index in range(len(df)):
            #===体の開きを計算===
            Nose = df.loc[index, 'Nose_x']                                                                #体の右端
            LEar = df.loc[index, 'LEar_x']                                                                     #体の左端
            REar = df.loc[index, 'REar_x']                                                                     #体の上端
            df.loc[index, 'LNdis'] = LEar - Nose                                                                     #体の下端
            df.loc[index, 'NRdis'] = Nose - REar                                  #体の幅
            df.loc[index, 'turning_face'] = df.loc[index, 'LNdis'] - df.loc[index, 'NRdis']

        # for index in range(len(df)):
        #     print(index, end=' ')
        #     if(have_got):
        #         if(np.isnan(df.loc[index, 'turning_body'])):
        #             pass
        #             print('nanpass')
        #         else:
        #             if(-5 <= df.loc[base_frame, 'turning_body'] - df.loc[index, 'turning_body'] and df.loc[base_frame, 'turning_body'] - df.loc[index, 'turning_body'] <= 5):
        #                 base_frame = index
        #                 df.loc[index, 'filterd_turning_body'] = df.loc[index, 'turning_body']
        #                 print('hanninai', end=' ')
        #                 if(checker):
        #                     df.loc[check_frame, 'filterd_turning_body'] = np.nan
        #                     print('delete', end='')
        #                 checker = 0
        #                 print()
        #             else:
        #                 if(checker):
        #                     if(-5 <= df.loc[check_frame, 'turning_body'] - df.loc[index, 'turning_body'] and df.loc[check_frame, 'turning_body'] - df.loc[index, 'turning_body'] <= 5):
        #                         base_frame = index
        #                         df.loc[check_frame, 'filterd_turning_body'] = df.loc[check_frame, 'turning_body']
        #                         df.loc[index, 'filterd_turning_body'] = df.loc[index, 'turning_body']
        #                         checker = 0
        #                         print('kakumei')
        #                     else:
        #                         df.loc[check_frame, 'filterd_turning_body'] = np.nan
        #                         check_frame = index
        #                         print('umm?')
        #                 else:
        #                     checker = 1
        #                     check_frame = index
        #                     print('checker on')
        #     else:
        #         if(not(np.isnan(df.loc[index, 'turning_body']))):
        #             have_got = 1
        #             base_frame = index
        #             df.loc[index, 'filterd_turning_body'] = df.loc[index, 'turning_body']
        #             print('start')
        # df['filterd_turning_body'] = df['filterd_turning_body'].interpolate()

        # # mini_filter(前方)
        # for i in range(move_area-1):
        #     move_list.append(df.loc[i, 'turning_body'])
        #     # print(str(i).zfill(4),move_list,df.loc[i, 'turning_body'])
        # for index in range(len(df)-move_area):
        #     move_list.append(df.loc[index+move_area-1, 'turning_body'])
        #     print(np.nanmin(move_list))
        #     df.loc[index, 'filterd_turning_body'] = np.nanmin(move_list)
        #     # print(str(index+4).zfill(4),move_list,df.loc[index, 'filterd_turning_bogy'])
        #     del(move_list[0])
        
        # # mini_filter(前後)
        # for i in range(move_area*2):
        #     move_list.append(df.loc[i, 'turning_body'])
        #     print(i)
        # for index in range(move_area,len(df)-move_area):
        #     print(index+move_area)
        #     move_list.append(df.loc[index+move_area, 'turning_body'])
        #     df.loc[index, 'filterd_turning_body'] = np.nanmin(move_list)
            # del(move_list[0])
            
        for i in range(move_area-1):
            move_list.append(df.loc[i, 'REar_x'])
            # print(str(i).zfill(4),move_list,df.loc[i, 'turning_body'])
        for index in range(len(df)-move_area):
            move_list.append(df.loc[index+move_area-1, 'REar_x'])
            print(np.nanmin(move_list))
            df.loc[index, 'filterd_REar_x'] = np.nanmax(move_list)
            # print(str(index+4).zfill(4),move_list,df.loc[index, 'filterd_turning_bogy'])
            del(move_list[0])

        for i in range(move_area-1):
            move_list.append(df.loc[i, 'turning_face'])
            # print(str(i).zfill(4),move_list,df.loc[i, 'turning_body'])
        for index in range(len(df)-move_area):
            move_list.append(df.loc[index+move_area-1, 'turning_face'])
            print(np.nanmin(move_list))
            df.loc[index, 'turning_face'] = np.nanmax(move_list)
            # print(str(index+4).zfill(4),move_list,df.loc[index, 'filterd_turning_bogy'])
            del(move_list[0])

        #===プロット===
        # turn_fig = plt.figure()
        # turn_ax = turn_fig.add_subplot(1,1,1)
        # df.plot('FrameNo', 'turning_body', c='#000', ax=turn_ax)

        # fil_turn_fig = plt.figure()
        # fil_turn_ax = fil_turn_fig.add_subplot(1,1,1)
        # df.plot('FrameNo', 'filterd_turning_body', c='#f00', ax=fil_turn_ax)

        # both_fig = plt.figure()
        # both_ax = both_fig.add_subplot(1,1,1)
        # df.plot('FrameNo', 'turning_body', c='#000', ax=both_ax)
        # df.plot('FrameNo', 'filterd_turning_body', c='#f00', ax=both_ax)

        face_fig = plt.figure()
        face_ax = face_fig.add_subplot(1,1,1)
        df.plot('FrameNo', 'REar_x', c='#00f', ax=face_ax)
        df.plot('FrameNo', 'LEar_x', c='#f00', ax=face_ax)
        df.plot('FrameNo', 'Nose_x', c='#000', ax=face_ax)

        face_dis_fig = plt.figure()
        face_dis_ax = face_dis_fig.add_subplot(1,1,1)
        # df.plot('FrameNo', 'LNdis', c='#00f', ax=face_dis_ax)
        # df.plot('FrameNo', 'NRdis', c='#f00', ax=face_dis_ax)
        df.plot('FrameNo', 'turning_face', c='#000', ax=face_dis_ax)

        # REar_x_fig = plt.figure()
        # REar_x_ax = REar_x_fig.add_subplot(1,1,1)
        # df.plot('FrameNo', 'REar_x', c='#000', ax=REar_x_ax)
        # df.plot('FrameNo', 'filterd_REar_x', c='#f00', ax=REar_x_ax)
        
        plt.show()

        # #===データベースに送信===
        # # コネクションの作成
        # conn = mydb.connect(host='localhost',port='3306',user='root',password='',database='SEN-KEN')
        # fl = fl.replace("\\", "/")
        # # DB操作用にカーソルを作成
        # cur = conn.cursor(buffered=True)

        # stmt = f"UPDATE 送信先のテーブル SET 体の開きが入るカラム = {df_csv[turning_body_list]} WHERE 条件;"
        # # print(stmt)
        # cur.execute(stmt)
        # cur.close()
        # conn.commit()
        # conn.close()
    print('done!')
print('all completed!')