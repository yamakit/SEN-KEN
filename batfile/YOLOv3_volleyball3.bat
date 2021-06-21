@echo off 
rem ******今%1になっているところを動画と同じ名前にリネームしておくこと。******
rem ******今0604になっているところは今日の日付にしておくこと。******************

rem Dドライブへ移動
cd /d D:

rem 各競技のフォルダへ移動
cd D:\htdocs\2021SEN_KEN\volleyball\1

rem ffmpegで作成した連番画像を保存するフォルダを作成
mkdir ffmpeg_%1

rem 作成したフォルダへの連番画像を作成するコマンド
ffmpeg -i D:\htdocs\2021SEN_KEN\volleyball\1\IMG_%1.MOV -r 30 D:\htdocs\2021SEN_KEN\volleyball\1\ffmpeg_%1\%%06d.jpg 

rem 画像へのPATHをテキストファイルに保存
dir /b /s ffmpeg_%1 > ffmpeg_%1.txt

rem Cドライブに戻る
C:

rem darknetを動かすフォルダへの移動
cd C:\darknet\build\darknet\x64

rem darknetの実行
darknet detector test "C:\darknet\build\darknet\x64\cfg\volleyballdetect.data" "C:\darknet\build\darknet\x64\cfg\yolov3-spp_volleyballdetect.cfg" "C:\darknet\build\darknet\x64\yolov3-spp_volleyballdetect_final.weights" < "D:\htdocs\2021SEN_KEN\volleyball\1\ffmpeg_%1.txt" -dont_show -thresh 0.9 -ext_output -out "D:\htdocs\2021SEN_KEN\volleyball\1\json\ffmpeg_%1.json

rem cd C:\openpose
rem mkdir D:\htdocs\2021SEN_KEN\volleyball\1\openpose_%1
rem bin\OpenPoseDemo.exe --video "D:\htdocs\2021SEN_KEN\volleyball\1\IMG_%1.MOV" --number_people_max 1 --tracking 0 --write_video D:\htdocs\2021SEN_KEN\volleyball\1\IMG_%1.avi --write_json "D:\htdocs\2021SEN_KEN\volleyball\1\openpose_%1"
rem mkdir openpose_%1
rem ffmpeg -i "D:\htdocs\2021SEN_KEN\volleyball\1\IMG_%1.avi" -r 30 D:\htdocs\2021SEN_KEN\volleyball\1\openpose_%1\%%06d.jpg 
