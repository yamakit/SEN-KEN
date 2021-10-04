import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import glob as gb
import mysql.connector as mydb
import os
import cv2
from multiprocessing import Pool

def keypoint_plot(*args):
    coors, fld_num, fle_num = args
    keyP_fig = plt.figure()
    keyP_ax = keyP_fig.add_subplot(1,1,1)
    keyP_ax.set_aspect('equal')
    keyP_ax.invert_yaxis()
    for index in range(int(len(coors)/3)):
        plt.plot(coors[index*3], coors[index*3+1], marker='.', axes=keyP_ax)
    plt.savefig(f'C:/Users/jagal/Desktop/graphs/keypoints/' + fld_num + '/' + str(fle_num).zfill(6))
    plt.clf()
    plt.close()

if __name__ == '__main__':
    #===DBからyolo_flagが1の動画のパスを取得===
    conn = mydb.connect(host='localhost',port='3306',user='root',password='',database='demo')
    cur = conn.cursor(buffered=True)
    cur.execute("SELECT video_path FROM yolo_video_table WHERE yolo_flag = 3")
    rows = cur.fetchall()
    folders = [] #jsonファイルへのパスを格納するリスト
    for row in rows:
        folders.append(row[0])
    cur.execute("UPDATE `yolo_video_table` SET `yolo_flag` = 4 WHERE `yolo_flag` = 3")
    cur.close
    conn.commit()
    conn.close()
    
    print(folders)

    #===データを取り出すjsonファイルが入っているフォルダー群を回す===
    for folder in folders:
        print(f'{folder}を処理')
        folder_num = folder[-8:-4]
        folder = folder.replace(folder[-12:],f'openpose_IMG_{folder_num}_01')
        folder = folder.replace('/', '\\')
        files_path = folder + '\\*.json'
        files = gb.glob(files_path)

        #===データフレームを用意===
        body_columns = ['FrameNo', 'Max_x', 'Min_x', 'Max_y', 'Min_y', 'MMbody', 'LsRsdis', 'MNsdis', 'Lsq', 'Rsq', 'dis_sq', 'LhMdis', 'MRhdis', 'LsNdis', 'NRsdis', 'turning_body', 'filterd_turning_body', 'LeNdis', 'NRedis', 'NoNedis', 'turning_face', 'filterd_turning_face', 'abs_turning_face', 'RhRbdis', 'LbLhdis']     #カラム名を用意
        body_columns_x = ['nose_x', 'neck_x', 'Rshoulder_x', 'Relbow_x', 'Rhand_x', 'Lshoulder_x', 'Lelbow_x', 'Lhand_x', 'Midhip_x', 'Rhip_x', 'Rknee_x', 'Rankle_x', 'Lhip_x', 'Lknee_x', 'Lankle_x', 'Reye_x', 'Leye_x', 'Rear_x', 'Lear_x', 'Lbigtoe_x', 'Lsmalltoe_x', 'Lheel_x', 'Rbigtoe_x', 'Rsmalltoe_x', 'Rheel_x']
        body_columns_y = ['nose_y', 'neck_y', 'Rshoulder_y', 'Relbow_y', 'Rhand_y', 'Lshoulder_y', 'Lelbow_y', 'Lhand_y', 'Midhip_y', 'Rhip_y', 'Rknee_y', 'Rankle_y', 'Lhip_y', 'Lknee_y', 'Lankle_y', 'Reye_y', 'Leye_y', 'Rear_y', 'Lear_y', 'Lbigtoe_y', 'Lsmalltoe_y', 'Lheel_y', 'Rbigtoe_y', 'Rsmalltoe_y', 'Rheel_y']
        folder_df = pd.DataFrame(index=range(len(files)))
        folder_df[body_columns] = np.nan                                                        #用意したカラム名の列を作成
        folder_df[body_columns_x] = np.nan
        folder_df[body_columns_y] = np.nan

        #===データ取り出し===
        for num,file in enumerate(files):
            print(num, end=' \n')        
            #===フォルダーからjsonファイルを取り出す===
            file_df = pd.read_json(file)
            people_data = file_df.loc[0, 'people']
            coor_list = people_data['pose_keypoints_2d']
            folder_df.loc[num, 'FrameNo'] = num
            if(file_df.empty == False):
                #===体の開きを計算===
                for index,column_names in enumerate(body_columns_x):
                    folder_df.loc[num, column_names] = coor_list[index*3]
                for index,column_names in enumerate(body_columns_y):
                    folder_df.loc[num, column_names] = coor_list[index*3+1]

                # if(num == 0):
                #     if not(os.path.exists(f'C:/Users/jagal/Desktop/graphs/keypoints/{folder_num}')):
                #         os.makedirs(f'C:/Users/jagal/Desktop/graphs/keypoints/{folder_num}')
                #     p = Pool()
                # p.apply(keypoint_plot, [coor_list, folder_num, num])
                # if(num % 100 == 0):
                #     p.close()
                #     p = Pool()
                # if(num+1 == len(files)):
                #     p.close()

                # folder_df.loc[num, 'Max_x'] = folder_df.loc[num, body_columns_x].max()
                # folder_df.loc[num, 'Min_x'] = folder_df.loc[num, body_columns_x].min()
                # folder_df.loc[num, 'Max_y'] = folder_df.loc[num, body_columns_y].max()
                # folder_df.loc[num, 'Min_y'] = folder_df.loc[num, body_columns_y].min()
                # folder_df.loc[num, 'MMbody'] = ((folder_df.loc[num, 'Max_x'] - folder_df.loc[num, 'Min_x']) / (folder_df.loc[num, 'Max_y'] - folder_df.loc[num, 'Min_y'])) * 100
                
                folder_df.loc[num, 'LsRsdis'] = folder_df.loc[num, 'Lshoulder_x'] - folder_df.loc[num, 'Rshoulder_x']   #左肩 - 右肩
                folder_df.loc[num, 'MNdis'] = folder_df.loc[num, 'Midhip_y'] - folder_df.loc[num, 'neck_y']             #首元 - 腰
                folder_df.loc[num, 'LsNdis'] = folder_df.loc[num, 'Lshoulder_x'] - folder_df.loc[num, 'neck_x']         #左肩 - 首元
                folder_df.loc[num, 'NRsdis'] = folder_df.loc[num, 'neck_x'] - folder_df.loc[num, 'Rshoulder_x']         #首元 - 右肩


                # if(folder_df.loc[num, 'LsNdis'] >= folder_df.loc[num, 'NRsdis']):
                #     folder_df.loc[num, 'turning_body'] = (folder_df.loc[num, 'LsRsdis'] / folder_df.loc[num, 'MNdis']) * -100 + 200
                # else:
                #     folder_df.loc[num, 'turning_body'] = (folder_df.loc[num, 'LsRsdis'] / folder_df.loc[num, 'MNdis']) * 100
                # folder_df.loc[num, 'turning_body'] = (folder_df.loc[num, 'LsRsdis'] / folder_df.loc[num, 'MNdis']) * 100
                # folder_df.loc[num, 'RhRb_dis'] = folder_df.loc[num, 'Rheel_x'] - folder_df.loc[num, 'Rbigtoe_x']
                # folder_df.loc[num, 'LbLh_dis'] = folder_df.loc[num, 'Lbigtoe_x'] - folder_df.loc[num, 'Lheel_x']
                # toto = folder_df.loc[num, 'RhRb_dis'] + folder_df.loc[num, 'LbLh_dis']

                # if(folder_df.loc[num, 'LsNdis'] >= folder_df.loc[num, 'NRsdis']):
                #     folder_df.loc[num, 'turning_body'] = (folder_df.loc[num, 'LsRsdis'] / folder_df.loc[num, 'MNdis']) * -100 + 200
                # else:
                #     folder_df.loc[num, 'turning_body'] = (folder_df.loc[num, 'LsRsdis'] / folder_df.loc[num, 'MNdis']) * 100
                folder_df.loc[num, 'turning_body'] = (folder_df.loc[num, 'LsRsdis'] / folder_df.loc[num, 'MNdis']) * 100
                folder_df.loc[num, 'filterd_turning_body'] = folder_df.loc[num, 'turning_body']

                if(folder_df.loc[num, 'turning_body'] < 0):
                    folder_df.loc[num, 'filterd_turning_body'] = 0
                if(folder_df.loc[num, 'turning_body'] > 100):
                    folder_df.loc[num, 'filterd_turning_body'] = 100

                #===顔の向きを計算===
                folder_df.loc[num, 'LeNdis'] = folder_df.loc[num, 'Lear_x'] - folder_df.loc[num, 'nose_x']            #左耳 - 鼻
                folder_df.loc[num, 'NRedis'] = folder_df.loc[num, 'nose_x'] - folder_df.loc[num, 'Rear_x']            #鼻 - 右耳
                folder_df.loc[num, 'NoNedis'] = folder_df.loc[num, 'nose_x'] - folder_df.loc[num, 'neck_x'] 

                folder_df.loc[num, 'turning_face'] = folder_df.loc[num, 'NoNedis']
                if(-50 <= folder_df.loc[num, 'NoNedis'] and folder_df.loc[num, 'NoNedis'] <= 50):
                    folder_df.loc[num, 'abs_turning_face'] = folder_df.loc[num, 'NoNedis']
                else:
                    folder_df.loc[num, 'abs_turning_face'] = 0

        folder_df['abs_turning_face'].abs()
        max_turning_face = folder_df['abs_turning_face'].max()
        for num,file in enumerate(files):
            folder_df.loc[num, 'filterd_turning_face'] = (folder_df.loc[num, 'turning_face'] / max_turning_face * 100) + 100

        move_list = []
        move_area = 5
        turning_body_list = []
        have_got = 0
        base_frame = 0
        checker = 0
        check_frame = 0
        str_json = ''
        found_path = ''
        folder_path = ''
        video_num = ''

        # move_list = []
        # for i in range(move_area-1):
        #     move_list.append(folder_df.loc[i, 'turning_face'])
        #     # print(str(i).zfill(4),move_list,df.loc[i, 'turning_body'])
        # for index in range(len(folder_df)-move_area):
        #     move_list.append(folder_df.loc[index+move_area-1, 'turning_face'])
        #     print(index+move_area-1, move_list)
        #     folder_df.loc[index, 'filterd_turning_face'] = np.nanmin(move_list)
        #     if(folder_df.loc[index, 'filterd_turning_face'] < 0):
        #        folder_df.loc[index, 'filterd_turning_face'] = 0
        #     if(folder_df.loc[index, 'filterd_turning_face'] > 200):
        #        folder_df.loc[index, 'filterd_turning_face'] = 200

        #     # print(str(index+4).zfill(4),move_list,df.loc[index, 'filterd_turning_bogy'])
        #     del(move_list[0])

        # body_fig = plt.figure()
        # body_ax = body_fig.add_subplot(1,1,1)
        # folder_df.plot('FrameNo', 'turning_body', c='#000', ax=body_ax)

        # filbody_fig = plt.figure()
        # filbody_ax = filbody_fig.add_subplot(1,1,1)
        # # folder_df.plot('FrameNo', 'MMbody', c='#f00', ax=filbody_ax, ylim=[0,200])
        # folder_df.plot('FrameNo', 'filterd_turning_body', c='#000', ax=filbody_ax, ylim=[0,100])

        # sq_fig = plt.figure()
        # sq_ax = sq_fig.add_subplot(1,1,1)
        # folder_df.plot('FrameNo', 'Rsq', c='#f00', ax=sq_ax)
        # folder_df.plot('FrameNo', 'Lsq', c='#000', ax=sq_ax)

        # hoge_fig = plt.figure()
        # hoge_ax = hoge_fig.add_subplot(1,1,1)
        # folder_df.plot('FrameNo', 'dis_sq', c='#90f32a', ax=hoge_ax)

        # dis_fig = plt.figure()
        # dis_ax = dis_fig.add_subplot(1,1,1)
        # folder_df.plot('FrameNo', 'LeNdis', c='#000', ax=dis_ax)
        # folder_df.plot('FrameNo', 'NRedis', c='#f00', ax=dis_ax)

        # face_fig = plt.figure()
        # face_ax = face_fig.add_subplot(1,1,1)
        # folder_df.plot('FrameNo', 'turning_face', c='#000', ax=face_ax)

        filface_fig = plt.figure()
        filface_ax = filface_fig.add_subplot(1,1,1)
        folder_df.plot('FrameNo', 'filterd_turning_face', c='#000', ax=filface_ax)
        
        # print(folder)
        plt.show()

        #===データベースに送信===
        # コネクションの作成
        conn = mydb.connect(host='localhost',port='3306',user='root',password='',database='SEN-KEN')
        # DB操作用にカーソルを作成
        cur = conn.cursor(buffered=True)
        body_json = folder_df['filterd_turning_face'].to_json()
        face_json = folder_df['filterd_turning_body'].to_json()
        folder = folder.replace('\\', '/')
        stmt = f"INSERT INTO `turning_body_table`(`turning_body_list`, `turning_face_list`, `video_path`) VALUES ('{body_json}', '{face_json}', '{folder}')"
        print(stmt)
        cur.execute(stmt)
        cur.close()
        conn.commit()
        conn.close()
        print('done!')
    print('all completed!')