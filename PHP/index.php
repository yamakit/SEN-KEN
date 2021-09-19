<?php
$ball_id = $_GET['ball_id'];
    
$dsn = 'mysql:dbname=sen-ken;host=localhost';
$user = 'root';
$password = '';
$result = array();

try {
    $dbh = new PDO($dsn, $user, $password);  

// 指定したball_idの動画のパス、動画の正解番号などの値を取得
    $sql = "SELECT * FROM picture as P,yolo_video_table as Y where P.video_id=Y.video_id AND ball_id = $ball_id ORDER BY RAND()";


    $stmt = $dbh->prepare($sql);
    $stmt->execute();
    $result = $stmt->fetchAll();

} catch (Exception $e) {
    echo $e->getMessage();
    exit();
}

header('Content-type: application/json');
echo json_encode($result,JSON_UNESCAPED_UNICODE);
?>

