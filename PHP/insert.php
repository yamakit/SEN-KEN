<?php
    // include 'db_config.php';

if(!empty($_GET)){
    $ball_id = $_GET['ball_id'];
    $video_id = $_GET['video_id'];
    $user_id = $_GET['user_id'];
    $button_id = $_GET['button_id'];
    $judge = $_GET['judge'];
    $x_coordinate = $_GET['x_coordinate'];
    $y_coordinate = $_GET['y_coordinate'];
    
    $dsn = 'mysql:dbname=sen-ken;host=localhost';
    $user = 'root';
    $password = '';
    $result = array();
    
    try {
        $dbh = new PDO($dsn, $user, $password);  
        
        // echo "<p>DB接続に成功しました。</p>";

        $sql = "INSERT INTO `answer_table`(`ball_id`, `yolo_video_id`, `user_id`, `button_id`, `ans_X_coordinate`, `ans_Y_coordinate`, `judge`, `datetime`) VALUES ($ball_id, $video_id, $user_id, $button_id,  $x_coordinate,  $y_coordinate, $judge, NOW())";
        $dbh->exec($sql);
    } catch (Exception $e) {
        // echo "<p>DB接続エラー</p>";
        echo $e->getMessage();
        exit();
    }
    
    header('Content-type: application/json');
    echo json_encode($result,JSON_UNESCAPED_UNICODE);
    // var_dump($result);
}
?>

