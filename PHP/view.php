<?php
    // include 'db_config.php';

    if(!empty($_GET)){
        $id = $_GET['player_id'];
        $hitplace = $_GET['hitplace'];

        $dsn = 'mysql:dbname=sen-ken;host=localhost';
        $user = 'root';
        $password = '';
        $result = array();

try {
    $dbh = new PDO($dsn, $user, $password);  

// echo "<p>DB接続に成功しました。</p>";
// $sql = "SELECT `ans_id`, `hitplace` FROM `yolo_video_table` WHERE `user_id` = $id";
$sql = "SELECT `ans_id` FROM `yolo_video_table` WHERE `player_id` = $id AND `hitplace`  = $hitplace ORDER BY `video_id` DESC LIMIT 100";


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
    }
?>

