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
        columns_list = df.columns.values
        X_columns = [col for index, col in enumerate(columns_list) if (index % 2 == 1)]            #val_listに入っている座標からx座標だけ取り出しX_valsに格納
        Y_columns = [col for index, col in enumerate(columns_list) if (index % 2 == 0 and not index == 0)]

        #===データフレームを用意===
        body_columns = ['Xmax','Xmin','Ymax','Ymin','width','height','turning_body', 'filterd_turning_body']     #カラム名を用意
        df[body_columns] = np.nan                                                        #用意したカラム名の列を作成

        for index in range(len(df)):
            X_vals = df.loc[index, X_columns]
            Y_vals = df.loc[index, Y_columns]
            #===体の開きを計算===
            df.loc[index, 'Xmax'] = max(X_vals)                                                                     #体の右端
            df.loc[index, 'Xmin'] = min(X_vals)                                                                     #体の左端
            df.loc[index, 'Ymax'] = max(Y_vals)                                                                     #体の上端
            df.loc[index, 'Ymin'] = min(Y_vals)                                                                     #体の下端
            df.loc[index, 'width'] = df.loc[index, 'Xmax'] - df.loc[index, 'Xmin']                                  #体の幅
            df.loc[index, 'height'] = df.loc[index, 'Ymax'] - df.loc[index, 'Ymin']
            if(df.loc[index, 'height'] != 0):
                df.loc[index, 'turning_body'] = float(df.loc[index, 'width']) / float(df.loc[index, 'height']) * 100    #体の開き

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

        for index in range(len(df)):
            print(index, end=' ')
            if(have_got):
                if(np.isnan(df.loc[index, 'turning_body'])):
                    pass
                    print('nanpass')
                else:
                    if(-5 <= df.loc[base_frame, 'turning_body'] - df.loc[index, 'turning_body'] and df.loc[base_frame, 'turning_body'] - df.loc[index, 'turning_body'] <= 5):
                        base_frame = index
                        df.loc[index, 'filterd_turning_body'] = df.loc[index, 'turning_body']
                        print('hanninai')
                    else:
                        df.loc[index, 'filterd_turning_body'] = np.nan
                        print('hannigai')
            else:
                if(not(np.isnan(df.loc[index, 'turning_body']))):
                    have_got = 1
                    base_frame = index
                    df.loc[index, 'filterd_turning_body'] = df.loc[index, 'turning_body']
                    print('start')
        df['filterd_turning_body'] = df['filterd_turning_body'].interpolate()

        #===プロット===
        # turn_fig = plt.figure()
        # turn_ax = turn_fig.add_subplot(1,1,1)
        # df.plot('FrameNo', 'turning_body', c='#000', ax=turn_ax)

        # fil_turn_fig = plt.figure()
        # fil_turn_ax = fil_turn_fig.add_subplot(1,1,1)
        # df.plot('FrameNo', 'filterd_turning_body', c='#f00', ax=fil_turn_ax)

        both_fig = plt.figure()
        both_ax = both_fig.add_subplot(1,1,1)
        df.plot('FrameNo', 'turning_body', c='#000', ax=both_ax)
        df.plot('FrameNo', 'filterd_turning_body', c='#f00', ax=both_ax)

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