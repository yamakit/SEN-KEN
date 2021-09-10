<?php
    // include 'db_config.php';

    if(!empty($_GET)){
        $id = $_GET['player_id'];
        $ball_id = $_GET['ball_id'];
        // $id2 = $_GET['randnum0'];
        // $id3 = $_GET['randnum1'];
        // $id4 = $_GET['randnum2'];
        // $id5 = $_GET['randnum3'];

        $dsn = 'mysql:dbname=sen-ken;host=localhost';
        $user = 'root';
        $password = '';
        $result = array();
        $result2 = array();
        // $result3 = array();
        // $result4 = array();
        // $result5 = array();

try {
    $dbh = new PDO($dsn, $user, $password);  

// echo "<p>DB接続に成功しました。</p>";

$sql = "SELECT * FROM `users` WHERE `id` = $id";
$stmt = $dbh->prepare($sql);
$stmt->execute();
$result = $stmt->fetchAll();

$sql2 = "SELECT * FROM `users` WHERE NOT (`id` = $id)  AND `ball_id` = $ball_id ORDER BY RAND() LIMIT 4";
$stmt2 = $dbh->prepare($sql2);
$stmt2->execute();
$result2 = $stmt2->fetchAll();

$result_arr = array($result, $result2);

} catch (Exception $e) {
//   echo "<p>DB接続エラー</p>";
echo $e->getMessage();
exit();
}

header('Content-type: application/json');
echo json_encode($result_arr,JSON_UNESCAPED_UNICODE);
    }
?>

