<?php
    // include 'db_config.php';
$ball_id = $_GET['ball_id'];
    
$dsn = 'mysql:dbname=sen-ken;host=localhost';
$user = 'root';
$password = '';
$result = array();

try {
    $dbh = new PDO($dsn, $user, $password);  

// echo "<p>DB接続に成功しました。</p>";

<<<<<<< HEAD
$sql = "SELECT * FROM `yolo_video_table` WHERE ball_id = $ball_id";
// $sql = "SELECT * FROM `yolo_video_table` ORDER BY RAND()";
=======
//$sql = "SELECT * FROM `yolo_video_table`";
//テスト用
//$sql = "SELECT * FROM `yolo_video_table` WHERE video_id BETWEEN 378 AND 417 ORDER BY RAND()";
//$sql = "SELECT * FROM `yolo_video_table` WHERE video_id = 105";
$sql = "SELECT * FROM `yolo_video_table` where ball_id = 1 ORDER BY RAND()";

>>>>>>> e52006e89b15fc563444c89595eccd927283b6dc
$stmt = $dbh->prepare($sql);
$stmt->execute();
$result = $stmt->fetchAll();

} catch (Exception $e) {
//   echo "<p>DB接続エラー</p>";
  echo $e->getMessage();
  exit();
}

header('Content-type: application/json');
echo json_encode($result,JSON_UNESCAPED_UNICODE);
// var_dump($result);
?>

