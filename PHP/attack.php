<?php
    include 'db_config.php';


$player_id = $_GET['player_id'];

$dsn = 'mysql:dbname=sen-ken;host=localhost';
$user = 'root';
$password = '';
$result = array();

try {
    $dbh = new PDO($dsn, $user, $password);  

// echo "<p>DB接続に成功しました。</p>";


$sql = "SELECT * FROM `yolo_video_table` WHERE player_id = $player_id LIMIT 50";
// $sql = "SELECT * FROM `yolo_video_table` WHERE player_id = 2";
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

