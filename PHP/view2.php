<?php

    if(!empty($_GET)){
        $path = $_GET['path'];
    
        $dsn = 'mysql:dbname=sen-ken;host=localhost';
        $user = 'root';
        $password = '';
        $result = array();

try {
    $dbh = new PDO($dsn, $user, $password);  

    // 指定した動画のパスの体の開きの値を取得
    $sql = "SELECT`turning_body_list`, `turning_face_list` FROM `turning_body_table` WHERE `video_path` = '$path'";
    $stmt = $dbh->prepare($sql);
    $stmt->execute();
    $result = $stmt->fetchAll();


} catch (Exception $e) {
echo $e->getMessage();
exit();
}

header('Content-type: application/json');
echo json_encode($result,JSON_UNESCAPED_UNICODE);
    }
?>

