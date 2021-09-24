@echo off

rem Dドライブに移動
d:

cd D:\htdocs\SEN-KEN\Python\

rem 以下はバレーボールの分析
python upload.py

python analysis.py

d:

cd D:\htdocs\SEN-KEN\Python\

python insert.py

python openpose.py



rem 以下はバドミントンの分析

d:

cd D:\htdocs\SEN-KEN\Python\

python upload_badminton.py

python analysis_badminton.py

python insert_badminton.py

python openpose_badminton.py