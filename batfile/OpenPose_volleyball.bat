@echo off

rem ********今%1になっている所を動画と同じ名前に置換する********
cd C:\openpose

rem OpenPose実行
bin\OpenPoseDemo.exe --video "D:\htdocs\2021SEN_KEN\volleyball\1\IMG_%1.MOV" --number_people_max 1 --tracking 0 --write_video D:\htdocs\2021SEN_KEN\volleyball\1\IMG_%1.avi --write_json "D:\htdocs\2021SEN_KEN\volleyball\1\openpose_%1"

rem フォルダを作成
mkdir D:\htdocs\2021SEN_KEN\volleyball\1\%1

rem 動画を分割
ffmpeg -i "D:\htdocs\2021SEN_KEN\volleyball\1\IMG_%1.avi" -r 30 D:\htdocs\2021SEN_KEN\volleyball\1\%1\%%06d.jpg

