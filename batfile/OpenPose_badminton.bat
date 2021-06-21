@echo off

rem ********今0203になっている所を動画と同じ名前に置換する********
rem ******今0514になっているところ変更しておくこと。**************

rem Dドライブへ移動
cd /d D:

cd D:\2021SEN_KEN\badminton

mkdir 0514

rem ダウンロードのフォルダに移動
cd "C:\Users\procon\Downloads"

rem ダウンロードのフォルダにファイルを移動
move IMG_0203.MOV D:\2021SEN_KEN\badminton\0514

rem Cドライブに戻る
C:

rem Openposeのフォルダに移動
cd C:\openpose

rem 出力したjsonが入るフォルダを作る
mkdir D:\2021SEN_KEN\badminton\0514\openpose_0203

rem OpenPose実行
bin\OpenPoseDemo.exe --video "D:\2021SEN_KEN\badminton\0514\IMG_0203.MOV" --number_people_max 1 --tracking 0 --write_video D:\2021SEN_KEN\badminton\0514\IMG_0203.avi --write_json "D:\2021SEN_KEN\badminton\0514\openpose_0203"

rem フォルダを作成
mkdir openpose_0203

rem 動画を分割
ffmpeg -i "D:\2021SEN_KEN\badminton\0514\IMG_0203.avi" -r 30 D:\2021SEN_KEN\badminton\0514\openpose_0203\%%06d.jpg 