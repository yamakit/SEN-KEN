<?php
    // include 'db_config.php';

        if(!empty($_GET)){
        $id = $_GET['player_id'];
        $day = $_GET['day'];

        $dsn = 'mysql:dbname=sen-ken;host=localhost';
        $user = 'root';
        $password = '';
        $result = array();
        $result2 = array();

try {
    $dbh = new PDO($dsn, $user, $password);  

// echo "DB接続に成功しました。";
$sql = "SELECT date_format(`datetime`,'%Y%m%d'),count(`judge`) FROM `answer_table` WHERE `user_id` = $id GROUP BY date_format(`datetime`,'%Y%m%d') ORDER BY `ans_id` DESC LIMIT $day";
$stmt = $dbh->prepare($sql);
$stmt->execute();
$result = $stmt->fetchAll();
$result2 = array_column($result, '1');

// var_dump($result2);
// var_dump($result);

} catch (Exception $e) {
// echo "DB接続エラー";
echo $e->getMessage();
exit();
}

header('Content-type: application/json');
echo json_encode($result2,JSON_UNESCAPED_UNICODE);
    }
?>

