<?php
//mysqlのパスワード
define('DB_USERNAME','root');
define('DB_PASSWORD','');
define('PDO_DSN','mysql:host=localhost;dbname=test;charset=utf8');
try
{
// mysql接続
$db = new PDO(PDO_DSN, DB_USERNAME, DB_PASSWORD);
$db->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

$begin = $_GET["begin"];
$stmt = $db->query("SELECT * FROM `answer_table` WHERE `user_id` = 2 LIMIT {$begin}");
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

?>