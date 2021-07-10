@echo off

rem ********今0247になっている所を動画と同じ名前に置換する********

rem Dドライブへ移動
cd /d D:

rem 各競技のフォルダへ移動
cd D:\2021SEN_KEN\softtennis

rem 日付のフォルダを作成
mkdir 0604

rem Cドライブに戻る
C:

rem ダウンロードのフォルダに移動
cd "C:\Users\procon\Downloads"

rem ダウンロードのフォルダにファイルを移動
move IMG_0247.MOV D:\2021SEN_KEN\softtennis\0604

rem Openposeのフォルダに移動
cd C:\openpose

rem 出力したjsonが入るフォルダを作る
mkdir D:\2021SEN_KEN\softtennis\0604\openpose_0247

rem OpenPose実行
bin\OpenPoseDemo.exe --video "D:\2021SEN_KEN\softtennis\0604\IMG_0247.MOV" --number_people_max 1 --tracking 0 --write_video D:\2021SEN_KEN\softtennis\0604\IMG_0247.avi --write_json "D:\2021SEN_KEN\softtennis\0604\openpose_0247"

rem フォルダを作成
mkdir openpose_0247

rem 動画を分割
ffmpeg -i "D:\2021SEN_KEN\softtennis\0604\IMG_0247.avi" -r 30 D:\2021SEN_KEN\softtennis\0604\openpose_0247\%%06d.jpg 