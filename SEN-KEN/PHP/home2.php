<?php

        if(!empty($_GET)){
        $id = $_GET['player_id'];
        $id2 = $_GET['randnum0'];
        $id3 = $_GET['randnum1'];
        $id4 = $_GET['randnum2'];
        $id5 = $_GET['randnum3'];

        $day = $_GET['day'];

        $dsn = 'mysql:dbname=sen-ken;host=localhost';
        $user = 'root';
        $password = '';
        $result = array();
        $data = array();
        $result2 = array();
        $data2 = array();
        $result3 = array();
        $data3 = array();
        $result4 = array();
        $data4 = array();
        $result5 = array();
        $data5 = array();

// 指定したidの人が解いた問題数を指定した直近の日数分取得
try {
$dbh = new PDO($dsn, $user, $password);  
$sql = "SELECT date_format(`datetime`,'%Y%m%d'),count(`judge`) FROM `answer_table` WHERE `user_id` = $id GROUP BY date_format(`datetime`,'%Y%m%d') ORDER BY `ans_id` DESC LIMIT $day";
$stmt = $dbh->prepare($sql);
$stmt->execute();
$result = $stmt->fetchAll();
$data = array_column($result, '1');

$sql2 = "SELECT date_format(`datetime`,'%Y%m%d'),count(`judge`) FROM `answer_table` WHERE `user_id` = $id2 GROUP BY date_format(`datetime`,'%Y%m%d') ORDER BY `ans_id` DESC LIMIT $day";
$stmt2 = $dbh->prepare($sql2);
$stmt2->execute();
$result2 = $stmt2->fetchAll();
$data2 = array_column($result2, '1');

$sql3 = "SELECT date_format(`datetime`,'%Y%m%d'),count(`judge`) FROM `answer_table` WHERE `user_id` = $id3 GROUP BY date_format(`datetime`,'%Y%m%d') ORDER BY `ans_id` DESC LIMIT $day";
$stmt3 = $dbh->prepare($sql3);
$stmt3->execute();
$result3 = $stmt3->fetchAll();
$data3 = array_column($result3, '1');

$sql4 = "SELECT date_format(`datetime`,'%Y%m%d'),count(`judge`) FROM `answer_table` WHERE `user_id` = $id4 GROUP BY date_format(`datetime`,'%Y%m%d') ORDER BY `ans_id` DESC LIMIT $day";
$stmt4 = $dbh->prepare($sql4);
$stmt4->execute();
$result4 = $stmt4->fetchAll();
$data4 = array_column($result4, '1');

$sql5 = "SELECT date_format(`datetime`,'%Y%m%d'),count(`judge`) FROM `answer_table` WHERE `user_id` = $id5 GROUP BY date_format(`datetime`,'%Y%m%d') ORDER BY `ans_id` DESC LIMIT $day";
$stmt5 = $dbh->prepare($sql5);
$stmt5->execute();
$result5 = $stmt5->fetchAll();
$data5 = array_column($result5, '1');

$data_arr = array($data, $data2, $data3, $data4, $data5);

} catch (Exception $e) {
echo $e->getMessage();
exit();
}

header('Content-type: application/json');
echo json_encode($data_arr,JSON_UNESCAPED_UNICODE);
    }
?>

