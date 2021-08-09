<?php
    // include 'db_config.php';

    
$dsn = 'mysql:dbname=test;host=localhost';
$user = 'root';
$password = '';
$result = array();

try {
    $dbh = new PDO($dsn, $user, $password);  

// echo "<p>DB接続に成功しました。</p>";

<<<<<<< HEAD
$sql = "SELECT * FROM `yolo_video_table`";
// $sql = "SELECT * FROM `yolo_video_table` ORDER BY RAND()";
=======
// $sql = "SELECT * FROM `yolo_video_table`";
$sql = "SELECT * FROM `yolo_video_tables` ORDER BY RAND()";
>>>>>>> dcd1d1adab5d6e4659122208fae70fa2f87fa43b
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

