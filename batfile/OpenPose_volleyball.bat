@echo off

rem ********今0203になっている所を動画と同じ名前に置換する********

rem ダウンロードのフォルダに移動
rem cd "C:\Users\procon\D
rem ダウンロードのフォルダにファイルを移動
rem move IMG_0203.MOV D:\2021SEN_KEN\volleyball\0514 


rem Openposeのフォルダに移動
cd C:\openpose

rem 出力したjsonが入るフォルダを作る
rem mkdir D:\htdocs\2021SEN_KEN\volleyball\1\openpose_0203

rem OpenPose実行
bin\OpenPoseDemo.exe --video "D:\htdocs\2021SEN_KEN\volleyball\1\IMG_0203.MOV" --number_people_max 1 --tracking 0 --write_video D:\htdocs\2021SEN_KEN\volleyball\1\IMG_0203.avi --write_json "D:\htdocs\2021SEN_KEN\volleyball\1\openpose_0203"

rem フォルダを作成
mkdir openpose_0203

rem 動画を分割
ffmpeg -i "D:\htdocs\2021SEN_KEN\volleyball\1\IMG_0203.avi" -r 30 D:\htdocs\2021SEN_KEN\volleyball\1\openpose_0203\%%06d.jpg