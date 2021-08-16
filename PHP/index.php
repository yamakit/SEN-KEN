<?php
    // include 'db_config.php';

    
$dsn = 'mysql:dbname=sen-ken;host=localhost';
$user = 'root';
$password = '';
$result = array();

try {
    $dbh = new PDO($dsn, $user, $password);  

// echo "<p>DB接続に成功しました。</p>";

//$sql = "SELECT * FROM `yolo_video_table`";
//テスト用
//$sql = "SELECT * FROM `yolo_video_table` WHERE video_id BETWEEN 378 AND 417 ORDER BY RAND()";
//$sql = "SELECT * FROM `yolo_video_table` WHERE video_id = 105";
$sql = "SELECT * FROM `yolo_video_table` where ball_id = 1 ORDER BY RAND()";

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

