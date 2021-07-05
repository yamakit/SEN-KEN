<?php
//mysqlのパスワード
define('DB_USERNAME','root');
define('DB_PASSWORD','');
<<<<<<< HEAD
define('PDO_DSN','mysql:host=localhost;dbname=SEN-KEN;charset=utf8');
=======
define('PDO_DSN','mysql:host=localhost;dbname=test;charset=utf8');
>>>>>>> demo
try
{
// mysql接続
$db = new PDO(PDO_DSN, DB_USERNAME, DB_PASSWORD);
$db->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

$begin = $_GET["begin"];
<<<<<<< HEAD
$stmt = $db->query("SELECT * FROM `answer_table` WHERE `user_id` = 1 LIMIT {$begin}");
=======
$stmt = $db->query("SELECT * FROM `answer_table` WHERE `user_id` = 2 LIMIT {$begin}");
>>>>>>> demo
$user_filtered = $stmt->fetchAll(PDO::FETCH_ASSOC);
    }
    catch(PDOException $e)
    {
    echo $e->getMessage();
    exit;
    $db = null;//接続を切る
    }

//echo $result[0]['correct_count'] . "/" . $result[0]['question_count']
header('Content-type: application/json');
$json = json_encode($user_filtered,JSON_UNESCAPED_UNICODE);
echo json_encode($user_filtered,JSON_UNESCAPED_UNICODE);

<<<<<<< HEAD
?>

=======
?>
>>>>>>> demo
