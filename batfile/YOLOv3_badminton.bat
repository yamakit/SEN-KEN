@echo off 
rem ******今0354になっているところを動画と同じ名前にリネームしておくこと。******
rem ******今1になっているところは今日の日付にしておくこと。******************

set /p NUMBER="INPUT:"

rem Dドライブへ移動
cd /d D:

rem 各競技のフォルダへ移動
cd D:\htdocs\2021SEN_KEN\badminton\1

rem 日付のフォルダを作成
mkdir ffmpeg_%NUMBER%

rem 作成したフォルダへの連番画像を作成するコマンド
ffmpeg -i D:\htdocs\2021SEN_KEN\badminton\1\IMG_%NUMBER%.MOV -r 30 D:\htdocs\2021SEN_KEN\badminton\1\ffmpeg_%NUMBER%\%%06d.jpg 

rem 画像へのPATHをテキストファイルに保存
dir /b /s ffmpeg_%NUMBER% > ffmpeg_%NUMBER%.txt

rem Cドライブに戻る
C:

rem darknetを動かすフォルダへの移動
cd C:\darknet\build\darknet\x64

rem darknetの実行
darknet detector test "C:\darknet\build\darknet\x64\cfg\shuttles.data" "C:\darknet\build\darknet\x64\cfg\shuttles.cfg" "C:\darknet\data\labelImage\shuttles_30000.weights" < "D:\htdocs\2021SEN_KEN\badminton\1\ffmpeg_%NUMBER%.txt" -dont_show -thresh 0.5 -ext_output -out "D:\htdocs\2021SEN_KEN\badminton\1\ffmpeg_%NUMBER%.json