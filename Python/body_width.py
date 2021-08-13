import pandas as pd
from pandas.io.json import json_normalize
import json
import numpy as np
import glob as gb
import mysql.connector as mydb

# files = gb.glob('目的のファイルが入っているフォルダーへのパス\\*.xlsx') #運用時の処理
folders = gb.glob('D:/htdocs/SEN-KEN/2021SEN_KEN/test/*.json')      #ローカル環境での実行用

#===データを取り出すjsonファイルが入っているフォルダー群を回す===
for folder in folders:
    #===フォルダーからjsonファイルを取り出す===
    print(f'{folder}内のファイルを処理')
    files = gb.glob(folder + '/*.json')
    turning_body_list = []                  #体の開きが入るリストを初期化
    for file in files:
        print(f'{file}を処理中... ', end='体の開き:')
        #===データ取り出し===
        df_json = pd.read_json(file)
        csv_path = file.replace('json', 'csv')      #jsonファイル読み込み
        df_json.to_csv(csv_path, encoding='utf-8')  #jsonからcsvに変換
        df_csv = pd.read_csv(csv_path)              
        if(df_csv.empty == False):
            csv_data_str = df_csv.loc[0, 'people']      #csvファイル読み込み
            triple = '''{}'''.format(csv_data_str)      
            csv_data = eval(triple)                     #文字列化しているデータを辞書型に変換
            val_list = csv_data["pose_keypoints_2d"]    #csv_data(辞書)から座標が入っているkeyのデータをリストに格納
        
            X_vals = [col for index, col in enumerate(val_list) if (index % 3 == 0)]            #val_listに入っている座標からx座標だけ取り出しX_valsに格納
            Y_vals = [col for index, col in enumerate(val_list) if (index % 3 == 1)]

            #===データフレームを用意===
            body_colums = ['Xmax','Xmin','Ymax','Ymin','width','height','turning_body']     #カラム名を用意
            df_csv[body_colums] = np.nan                                                    #用意したカラム名の列を作成

            #===体の開きを計算===
            Xmax = max(X_vals)                                  #体の右端
            Xmin = min(X_vals)                                  #体の左端
            Ymax = max(Y_vals)                                  #体の上端
            Ymin = min(Y_vals)                                  #体の下端
            width = Xmax - Xmin                                 #体の幅
            print(width)
            height = Ymax - Ymin
            print(height)                                #体の高さ
            turning_body = float(width) / float(height) * 100   #体の開き
            print(turning_body)
            turning_body_list.append(turning_body)              #取得した体の開きをturning_body_listに追加
        else:
            turning_body_list.append(np.nan)
        print(turning_body_list[-1])

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