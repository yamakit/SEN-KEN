<?php

    if(!empty($_GET)){
        $path = $_GET['path'];
    
        $dsn = 'mysql:dbname=sen-ken;host=localhost';
        $user = 'root';
        $password = '';
        $result = array();

try {
    $dbh = new PDO($dsn, $user, $password);  
    $sql = "SELECT `turning_body_list` FROM `turning_body_table` WHERE `video_path` = '$path'";


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

