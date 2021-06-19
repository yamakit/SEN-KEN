<?php
// include 'db_config.php';
$food_name = $_POST['SelectPref'];
echo($food_name);

header('Content-type: application/json');
echo json_encode($food_name,JSON_UNESCAPED_UNICODE);
// $sport = $_POST['sport'];
// session_start();

// $dsn = 'mysql:dbname=yolo_video_table;host=localhost';
// $user = 'root';
// $password = '';

// try {
   
//     $dbh = new PDO($dsn, $user, $password);  

//   $sql = "SELECT * FROM `users` WHERE id = $food_name";
//   $stmt = $dbh->query($sql); //挿入する値は空のまま、SQL実行の準備をする
//   $product = $stmt->fetch(PDO::FETCH_ASSOC);
//   $name = $product['plyaer_id'];

//   $sql_list = $stmt->fetchAll();

// } catch (Exception $e) {
//     echo $e->getMessage();
//     exit();
//   }

// $sql2 = "SELECT * FROM `ball_games` WHERE id = $sport";
// $stmt2 = $pdo->query($sql2); //挿入する値は空のまま、SQL実行の準備をする
// $product2 = $stmt2->fetch(PDO::FETCH_ASSOC);
// $name2 = $product2['ball_game'];

// $dbh = null;

?>

<!-- <!doctype html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="Cache-Control" content="no-cache">
<title>
せえええええい
</title>
</head>
<body>
 <h1>
<?php echo $food_name?>番の人が使っています。
</h1> 

</body>  -->