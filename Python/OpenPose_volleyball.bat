@echo off

C: 
rem ********今%1になっている所を動画と同じ名前に置換する********
cd C:\openpose

rem OpenPose実行
bin\OpenPoseDemo.exe --video "D:\htdocs\SEN-KEN\2021SEN_KEN\volleyball\%1\%2.MOV" --tracking 0 --write_video "D:\htdocs\SEN-KEN\2021SEN_KEN\volleyball\%1\%2.avi" --write_json "D:\htdocs\SEN-KEN\2021SEN_KEN\volleyball\%1\openpose_%2" --number_people_max 1
echo bin\OpenPoseDemo.exe --video "D:\htdocs\SEN-KEN\2021SEN_KEN\volleyball\%1\%2.MOV" --write_video "D:\htdocs\SEN-KEN\2021SEN_KEN\volleyball\%1\%2.avi" --write_json "D:\htdocs\SEN-KEN\2021SEN_KEN\volleyball\%1\openpose_%2"

rem フォルダを作成
mkdir D:\htdocs\SEN-KEN\2021SEN_KEN\volleyball\%1\openpose_%2

rem 動画を分割
ffmpeg -i "D:\htdocs\SEN-KEN\2021SEN_KEN\volleyball\%1\%2.avi" -r 30 D:\htdocs\SEN-KEN\2021SEN_KEN\volleyball\%1\openpose_%2\OpenPose_%%06d.jpg

