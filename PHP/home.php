<?php
    // include 'db_config.php';

    if(!empty($_GET)){
        $id = $_GET['player_id'];

        $dsn = 'mysql:dbname=sen-ken;host=localhost';
        $user = 'root';
        $password = '';
        $result = array();

try {
    $dbh = new PDO($dsn, $user, $password);  

// echo "<p>DB接続に成功しました。</p>";

$sql = "SELECT`ball_id`FROM `users` WHERE `id` = $id";

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

