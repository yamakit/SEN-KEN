<?php


$player_id = $_GET['player_id'];

$dsn = 'mysql:dbname=sen-ken;host=localhost';
$user = 'root';
$password = '';
$result = array();

try {
    $dbh = new PDO($dsn, $user, $password);  



//直近100本の動画のパス、ボールが通った座標などの値を取得
// $sql = "SELECT * FROM `yolo_video_table` WHERE player_id = $player_id ORDER BY `video_id` DESC LIMIT 100";
$sql = "SELECT * FROM `yolo_video_table` WHERE player_id = $player_id LIMIT 20";
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

