<?php
    include 'db_config.php';

    $dsn = 'mysql:dbname=test;host=localhost';
$user = 'root';
$password = '';
$result = array();

try {
    $dbh = new PDO($dsn, $user, $password);  

  $sql = "SELECT * FROM `users`";
  $stmt = ($dbh->prepare($sql));
  $stmt->execute();


  $sql_list = $stmt->fetchAll();

} catch (Exception $e) {
    echo $e->getMessage();
    exit();
  }
  
  header('Content-type: application/json');
  echo json_encode($sql_list,JSON_UNESCAPED_UNICODE);
?>