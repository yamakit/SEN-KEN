<?php
    // include 'db_config.php';

        if(!empty($_GET)){
        $id = $_GET['player_id'];
        $id2 = $_GET['randnum0'];
        $id3 = $_GET['randnum1'];
        $id4 = $_GET['randnum2'];
        $id5 = $_GET['randnum3'];
        $sum = $_GET['sum'];
        $sum2 = $_GET['sum2'];
        $sum3= $_GET['sum3'];
        $sum4 = $_GET['sum4'];
        $sum5 = $_GET['sum5'];

        $dsn = 'mysql:dbname=sen-ken;host=localhost';
        $user = 'root';
        $password = '';
        // $result = array();
        $result = array();
        $result2 = array();
        $result3 = array();
        $result4 = array();
        $result5 = array();

try {
    $dbh = new PDO($dsn, $user, $password);  


$sql = "SELECT * FROM `answer_table` WHERE `user_id` = $id ORDER BY `datetime` DESC LIMIT $sum";
$stmt = $dbh->prepare($sql);
$stmt->execute();
$result = $stmt->fetchAll();

$sql2 = "SELECT * FROM `answer_table` WHERE `user_id` = $id2 ORDER BY `datetime` DESC LIMIT $sum2";
$stmt2 = $dbh->prepare($sql2);
$stmt2->execute();
$result2 = $stmt2->fetchAll();

$sql3 = "SELECT * FROM `answer_table` WHERE `user_id` = $id3 ORDER BY `datetime` DESC LIMIT $sum3";
$stmt3 = $dbh->prepare($sql3);
$stmt3->execute();
$result3 = $stmt3->fetchAll();

$sql4 = "SELECT * FROM `answer_table` WHERE `user_id` = $id4 ORDER BY `datetime` DESC LIMIT $sum4";
$stmt4 = $dbh->prepare($sql4);
$stmt4->execute();
$result4 = $stmt4->fetchAll();

$sql5 = "SELECT * FROM `answer_table` WHERE `user_id` = $id5 ORDER BY `datetime` DESC LIMIT $sum5";
$stmt5 = $dbh->prepare($sql5);
$stmt5->execute();
$result5 = $stmt5->fetchAll();

$result_arr = array($result, $result2, $result3, $result4, $result5);

} catch (Exception $e) {
// echo "DB接続エラー";
echo $e->getMessage();
exit();
}

header('Content-type: application/json');
echo json_encode($result_arr,JSON_UNESCAPED_UNICODE);
    }
?>

