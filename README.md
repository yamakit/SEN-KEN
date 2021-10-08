# SEN-KEN

pythonの各ファイルの機能

- ### upload.py  
　新しくフォルダに追加された動画のPATHをDBに挿入します。  

- ### analysis.py  
　DBからYOLOv3を掛けていない動画を取得し、動画に対してYOLOv３を掛けてボールの座標をjsonファイルで出力します。  

- ### insert.py
  analysis.pyで出力されたファイルから、スパイクのフレームを検出し、それに関する情報をDBに挿入します。 

- ### openpose.py
  DBからopenposeを掛けていない動画を取得し、動画に対してopenposeを掛けてボールの座標をjsonファイルで出力します。  

- ### body_width.py  
  openpose.pyで出力されたファイルから、体の開きと顔の向きを計算し、DBに挿入します。  

- ### pick_frame1img.py
   DBから、ボールが打たれた瞬間のフレームを取得し、そのフレームの画像のパスをDBに挿入します。  

- ### upload_badminton.py
  upload.pyのバドミントン用です。  
  
- ### analysis_badminton.py
  analysis.pyのバドミントン用です。  
  
- ### insert_badminton.py
  upload.pyのバドミントン用です。  
  
- ### openpose_badminton.py
  openpose.pyのバドミントン用です。  
