import json as j
from decimal import Decimal

json_open = open('./ffmpeg_0202.json','r')
json_load = j.load(json_open)

data_list = [] #フレームの比較結果 [0:[前frameからの経過,x座標の変位],1:[前frameからの経過,x座標の変位],2:...]
listA = [] #比較するフレームの若い方のデータ 　[frame数,x座標,y座標]
listB = [] #比較するフレームの老けた方のデータ [frame数,x座標,y座標]
setup_step = 0

for frame in json_load: #frame(辞書型)
    if frame["objects"]: #objectsに要素があるか
        if setup_step == 0:
            listA = [frame["frame_id"],frame["objects"][0]["relative_coordinates"]["center_x"],frame["objects"][0]["relative_coordinates"]["center_y"]]
            listA[1] = Decimal(str(listA[1]))
            listA[2] = Decimal(str(listA[2]))
            setup_step = 1
        elif setup_step == 1:
            listB = [frame["frame_id"],str(frame["objects"][0]["relative_coordinates"]["center_x"]),str(frame["objects"][0]["relative_coordinates"]["center_y"])]
            listB[1] = Decimal(str(listB[1]))
            listB[2] = Decimal(str(listB[2]))
            ansX = listB[1] - listA[1]
            ansY = listB[2] - listA[2]
            data_list.append([listB[0] - listA[0],float(ansX),float(ansY)])
            listA = listB
            setup_step = 2
        else:
            listB = [frame["frame_id"],str(frame["objects"][0]["relative_coordinates"]["center_x"]),str(frame["objects"][0]["relative_coordinates"]["center_y"])]
            listB[1] = Decimal(str(listB[1]))
            listB[2] = Decimal(str(listB[2]))
            ansX = listB[1] - listA[1]
            ansY = listB[2] - listA[2]
            data_list.append([listB[0] - listA[0],float(ansX),float(ansY)])
            listA = listB

print(data_list)

with open('mydata.json', mode='wt', encoding='utf-8') as file:
    j.dump(data_list, file, ensure_ascii=False, indent=2)
