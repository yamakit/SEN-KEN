# SEN-KEN

pythonの各ファイルの機能

・upload.py
　新しくフォルダに追加された動画のPATHをDBに挿入します。

・analysis.py
　DBから物体検出ライブラリであるYOLOv3を掛けていない動画を取得し、その動画に対してYOLOv３を掛けてボールの座標をテキストファイルで出力します。
