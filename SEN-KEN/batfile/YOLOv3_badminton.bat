@echo off 
rem Dドライブへ移動
cd /d D:

rem 各競技のフォルダへ移動
cd D:\htdocs\2021SEN_KEN\badminton\1

rem ffmpegで作成した連番画像を保存するフォルダを作成
mkdir ffmpeg_%1

rem 作成したフォルダへの連番画像を作成するコマンド
ffmpeg -i D:\htdocs\2021SEN_KEN\badminton\1\IMG_%1.MOV -r 30 D:\htdocs\2021SEN_KEN\badminton\1\ffmpeg_%1\%%06d.jpg 

rem 画像へのPATHをテキストファイルに保存
dir /b /s ffmpeg_%1 > ffmpeg_%1.txt

rem Cドライブに戻る
C:

rem darknetを動かすフォルダへの移動
cd C:\darknet\build\darknet\x64

rem darknetの実行
darknet detector test "C:\darknet\build\darknet\x64\cfg\shuttles.data" "C:\darknet\build\darknet\x64\cfg\shuttles.cfg" "C:\darknet\data\labelImage\shuttles_30000.weights" < "D:\htdocs\2021SEN_KEN\badminton\1\ffmpeg_%1.txt" -dont_show -thresh 0.9 -ext_output -out "D:\htdocs\2021SEN_KEN\badminton\1\ffmpeg_%1.json
