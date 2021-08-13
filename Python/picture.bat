@echo off 
rem Dドライブへ移動
rem cd /d D:

rem 画像が入っているフォルダへ移動
rem cd D:\htdocs\SEN-KEN\2021SEN_KEN\volleyball\%1\%2

rem ffmpegで作成した連番画像を保存するフォルダを作成
rem mkdir %1

rem 作成したフォルダへの連番画像を作成するコマンド
rem 変えてほしい
rem ffmpeg -i D:\htdocs\SEN-KEN\2021SEN_KEN\volleyball\%1\%2.MOV -r 30 D:\htdocs\SEN-KEN\2021SEN_KEN\volleyball\%1\%2\%%05d.jpg 

rem 画像へのPATHをテキストファイルに保存
rem dir /b /s %2  %2.txt

rem Cドライブに戻る
C:

rem darknetを動かすフォルダへの移動
cd C:\darknet\build\darknet\x64

rem darknetの実行
rem 変えてほしい
darknet detector test "cfg/coco.data" "cfg/yolov3.cfg" "yolov3.weights" "D:\htdocs\SEN-KEN\2021SEN_KEN\volleyball\%1\%2\%3.jpg" -dont_show -thresh 0.9 -ext_output -out "D:\htdocs\SEN-KEN\2021SEN_KEN\volleyball\%1\%2\%3.json"
echo "D:\htdocs\SEN-KEN\2021SEN_KEN\volleyball\%1\%2\%3.json"

cd /d D:
cd D:\htdocs\SEN-KEN\Python\