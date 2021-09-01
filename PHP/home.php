<?php
    // include 'db_config.php';

    if(!empty($_GET)){
        $id = $_GET['player_id'];
        $id2 = $_GET['randnum0'];
        $id3 = $_GET['randnum1'];
        $id4 = $_GET['randnum2'];
        $id5 = $_GET['randnum3'];

        $dsn = 'mysql:dbname=sen-ken;host=localhost';
        $user = 'root';
        $password = '';
        $result = array();
        $result2 = array();
        $result3 = array();
        $result4 = array();
        $result5 = array();

try {
    $dbh = new PDO($dsn, $user, $password);  

// echo "<p>DB接続に成功しました。</p>";

$sql = "SELECT * FROM `users` WHERE `id` = $id";
$stmt = $dbh->prepare($sql);
$stmt->execute();
$result = $stmt->fetchAll();

$sql2 = "SELECT `name` FROM `users` WHERE `id` = $id2";
$stmt2 = $dbh->prepare($sql2);
$stmt2->execute();
$result2 = $stmt2->fetchAll();

$sql3 = "SELECT `name` FROM `users` WHERE `id` = $id3";
$stmt3 = $dbh->prepare($sql3);
$stmt3->execute();
$result3 = $stmt3->fetchAll();

$sql4 = "SELECT `name` FROM `users` WHERE `id` = $id4";
$stmt4 = $dbh->prepare($sql4);
$stmt4->execute();
$result4 = $stmt4->fetchAll();

$sql5 = "SELECT `name` FROM `users` WHERE `id` = $id5";
$stmt5 = $dbh->prepare($sql5);
$stmt5->execute();
$result5 = $stmt5->fetchAll();

$result_arr = array($result, $result2, $result3, $result4, $result5);

} catch (Exception $e) {
//   echo "<p>DB接続エラー</p>";
echo $e->getMessage();
exit();
}

header('Content-type: application/json');
echo json_encode($result_arr,JSON_UNESCAPED_UNICODE);
// var_dump($result);
    }
?>

