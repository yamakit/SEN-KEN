<?php

    if(!empty($_GET)){
        $id = $_GET['player_id'];

        $dsn = 'mysql:dbname=sen-ken;host=localhost';
        $user = 'root';
        $password = '';
        $result = array();
        $result2 = array();

try {
    $dbh = new PDO($dsn, $user, $password);  

// 指定したidのball_id、名前、画像のパスなどの値を取得
$sql = "SELECT * FROM `users` WHERE `id` = $id";
$stmt = $dbh->prepare($sql);
$stmt->execute();
$result = $stmt->fetchAll();

// 指定したid以外で、指定したball_idと同じball_idのid、名前などの値をランダムで取得
$sql2 = "SELECT * FROM `users` WHERE NOT (`id` = $id)  AND `ball_id` = {$result[0]["ball_id"]} ORDER BY RAND() LIMIT 4";
$stmt2 = $dbh->prepare($sql2);
$stmt2->execute();
$result2 = $stmt2->fetchAll();

$result_arr = array($result, $result2);

} catch (Exception $e) {
echo $e->getMessage();
exit();
}

header('Content-type: application/json');
echo json_encode($result_arr,JSON_UNESCAPED_UNICODE);
    }
?>

