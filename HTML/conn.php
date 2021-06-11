<?php
     //mysqlのパスワード
     define('DB_USERNAME','root');
     define('DB_PASSWORD','');
     define('PDO_DSN','mysql:host=localhost;dbname=SEN-KEN;charset=utf8');

?>
    <?php

try
{
   // mysql接続
   $db = new PDO(PDO_DSN, DB_USERNAME, DB_PASSWORD);
   $db->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
  //ユーザー1が解いた全問題でbutton1を通った数
   $stmt = $db->query("SELECT COUNT(button_id) FROM `answer_table` WHERE button_id = 1 AND ball_id = 1 AND user_id = 1");
   $button1_bunbo = $stmt->fetch(PDO::FETCH_ASSOC);
   // var_dump($a);
   $button1_tuuka = $button1_bunbo['COUNT(button_id)'];
    }
    catch(PDOException $e)
    {
     echo $e->getMessage();
     exit;
       $db = null;//接続を切る
    }

?>
<?php
  try
  {
  //ユーザー1がといた全問題でbutton1が正解した数
   $stmt2 = $db->query("SELECT COUNT(button_id) FROM `answer_table` WHERE button_id = 1 AND flag = 1 AND ball_id = 1 AND user_id = 1");
   $button1_bunsi = $stmt2->fetch(PDO::FETCH_ASSOC);
 
   $button1_seikai = $button1_bunsi['COUNT(button_id)'];

   $db = null;
  }
  catch(PDOException $e)
  {
  echo $e->getMessage();
  exit;
  }
?>
<?php

try
{
   // mysql接続
   $db = new PDO(PDO_DSN, DB_USERNAME, DB_PASSWORD);
   $db->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

   $stmt3 = $db->query("SELECT COUNT(button_id) FROM `answer_table` WHERE button_id = 2 AND ball_id = 1 AND user_id = 1");
   $button2_bunbo = $stmt3->fetch(PDO::FETCH_ASSOC);
   // var_dump($a);
   $button2_tuuka = $button2_bunbo['COUNT(button_id)'];
  
   //接続を切る
   //$db = null;
    }
    catch(PDOException $e)
    {
     echo $e->getMessage();
     exit;
       $db = null;//接続を切る
    }

?>
<?php
  try
  {
 
   $stmt4 = $db->query("SELECT COUNT(button_id) FROM `answer_table` WHERE button_id = 2 AND flag = 1 AND ball_id = 1 AND user_id = 1");
   $button2_bunsi = $stmt4->fetch(PDO::FETCH_ASSOC);
 
   $button2_seikai = $button2_bunsi['COUNT(button_id)'];

   $db = null;
  }
  catch(PDOException $e)
  {
  echo $e->getMessage();
  exit;
  }
?>
<?php

try
{
   // mysql接続
   $db = new PDO(PDO_DSN, DB_USERNAME, DB_PASSWORD);
   $db->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

   $stmt5 = $db->query("SELECT COUNT(button_id) FROM `answer_table` WHERE button_id = 3 AND ball_id = 1 AND user_id = 1");
   $button3_bunbo = $stmt5->fetch(PDO::FETCH_ASSOC);
   // var_dump($a);
   $button3_tuuka = $button3_bunbo['COUNT(button_id)'];
  
   //接続を切る
   //$db = null;
    }
    catch(PDOException $e)
    {
     echo $e->getMessage();
     exit;
       $db = null;//接続を切る
    }

?>
<?php
  try
  {
 
   $stmt6 = $db->query("SELECT COUNT(button_id) FROM `answer_table` WHERE button_id = 3 AND flag = 1 AND ball_id = 1 AND user_id = 1");
   $button3_bunsi = $stmt6->fetch(PDO::FETCH_ASSOC);
 
   $button3_seikai = $button3_bunsi['COUNT(button_id)'];

   $db = null;
  }
  catch(PDOException $e)
  {
  echo $e->getMessage();
  exit;
  }
?>
<?php

try
{
   // mysql接続
   $db = new PDO(PDO_DSN, DB_USERNAME, DB_PASSWORD);
   $db->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

   $stmt7 = $db->query("SELECT COUNT(button_id) FROM `answer_table` WHERE button_id = 4 AND ball_id = 1 AND user_id = 1");
   $button4_bunbo = $stmt7->fetch(PDO::FETCH_ASSOC);
   // var_dump($a);
   $button4_tuuka = $button4_bunbo['COUNT(button_id)'];
  
   //接続を切る
   //$db = null;
    }
    catch(PDOException $e)
    {
     echo $e->getMessage();
     exit;
       $db = null;//接続を切る
    }

?>
<?php
  try
  {
 
   $stmt8 = $db->query("SELECT COUNT(button_id) FROM `answer_table` WHERE button_id = 4 AND flag = 1 AND ball_id = 1 AND user_id = 1");
   $button4_bunsi = $stmt8->fetch(PDO::FETCH_ASSOC);
 
   $button4_seikai = $button4_bunsi['COUNT(button_id)'];

   $db = null;
  }
  catch(PDOException $e)
  {
  echo $e->getMessage();
  exit;
  }
?>
<?php

try
{
   // mysql接続
   $db = new PDO(PDO_DSN, DB_USERNAME, DB_PASSWORD);
   $db->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

   $stmt9 = $db->query("SELECT COUNT(button_id) FROM `answer_table` WHERE button_id = 5 AND ball_id = 1 AND user_id = 1");
   $button5_bunbo = $stmt9->fetch(PDO::FETCH_ASSOC);
   // var_dump($a);
   $button5_tuuka = $button5_bunbo['COUNT(button_id)'];
  
   //接続を切る
   //$db = null;
    }
    catch(PDOException $e)
    {
     echo $e->getMessage();
     exit;
       $db = null;//接続を切る
    }

?>
<?php
  try
  {
 
   $stmt10 = $db->query("SELECT COUNT(button_id) FROM `answer_table` WHERE button_id = 5 AND flag = 1 AND ball_id = 1 AND user_id = 1");
   $button5_bunsi = $stmt10->fetch(PDO::FETCH_ASSOC);
 
   $button5_seikai = $button4_bunsi['COUNT(button_id)'];

   $db = null;
  }
  catch(PDOException $e)
  {
  echo $e->getMessage();
  exit;
  }
?>
<?php

try
{
   // mysql接続
   $db = new PDO(PDO_DSN, DB_USERNAME, DB_PASSWORD);
   $db->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

   $stmt11 = $db->query("SELECT COUNT(button_id) FROM `answer_table` WHERE button_id = 6 AND ball_id = 1 AND user_id = 1");
   $button6_bunbo = $stmt11->fetch(PDO::FETCH_ASSOC);
   // var_dump($a);
   $button6_tuuka = $button6_bunbo['COUNT(button_id)'];
  
   //接続を切る
   //$db = null;
    }
    catch(PDOException $e)
    {
     echo $e->getMessage();
     exit;
       $db = null;//接続を切る
    }

?>
<?php
  try
  {
 
   $stmt12 = $db->query("SELECT COUNT(button_id) FROM `answer_table` WHERE button_id = 6 AND flag = 1 AND ball_id = 1 AND user_id = 1");
   $button6_bunsi = $stmt12->fetch(PDO::FETCH_ASSOC);
 
   $button6_seikai = $button6_bunsi['COUNT(button_id)'];

   $db = null;
  }
  catch(PDOException $e)
  {
  echo $e->getMessage();
  exit;
  }
?>
<?php

try
{
   // mysql接続
   $db = new PDO(PDO_DSN, DB_USERNAME, DB_PASSWORD);
   $db->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

   $stmt13 = $db->query("SELECT COUNT(button_id) FROM `answer_table` WHERE button_id = 7 AND ball_id = 1 AND user_id = 1");
   $button7_bunbo = $stmt13->fetch(PDO::FETCH_ASSOC);
   // var_dump($a);
   $button7_tuuka = $button7_bunbo['COUNT(button_id)'];
  
   //接続を切る
   //$db = null;
    }
    catch(PDOException $e)
    {
     echo $e->getMessage();
     exit;
       $db = null;//接続を切る
    }

?>
<?php
  try
  {
 
   $stmt14 = $db->query("SELECT COUNT(button_id) FROM `answer_table` WHERE button_id = 7 AND flag = 1 AND ball_id = 1 AND user_id = 1");
   $button7_bunsi = $stmt14->fetch(PDO::FETCH_ASSOC);
 
   $button7_seikai = $button6_bunsi['COUNT(button_id)'];

   $db = null;
  }
  catch(PDOException $e)
  {
  echo $e->getMessage();
  exit;
  }
?>
<?php

try
{
   // mysql接続
   $db = new PDO(PDO_DSN, DB_USERNAME, DB_PASSWORD);
   $db->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

   $stmt15 = $db->query("SELECT COUNT(button_id) FROM `answer_table` WHERE button_id = 8 AND ball_id = 1 AND user_id = 1");
   $button8_bunbo = $stmt15->fetch(PDO::FETCH_ASSOC);
   // var_dump($a);
   $button8_tuuka = $button8_bunbo['COUNT(button_id)'];
  
   //接続を切る
   //$db = null;
    }
    catch(PDOException $e)
    {
     echo $e->getMessage();
     exit;
       $db = null;//接続を切る
    }

?>
<?php
  try
  {
 
   $stmt16 = $db->query("SELECT COUNT(button_id) FROM `answer_table` WHERE button_id = 8 AND flag = 1 AND ball_id = 1 AND user_id = 1");
   $button8_bunsi = $stmt16->fetch(PDO::FETCH_ASSOC);
 
   $button8_seikai = $button8_bunsi['COUNT(button_id)'];

   $db = null;
  }
  catch(PDOException $e)
  {
  echo $e->getMessage();
  exit;
  }
?>
<?php

try
{
   // mysql接続
   $db = new PDO(PDO_DSN, DB_USERNAME, DB_PASSWORD);
   $db->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

   $stmt17 = $db->query("SELECT COUNT(button_id) FROM `answer_table` WHERE button_id = 9 AND ball_id = 1 AND user_id = 1");
   $button9_bunbo = $stmt17->fetch(PDO::FETCH_ASSOC);
   // var_dump($a);
   $button9_tuuka = $button9_bunbo['COUNT(button_id)'];
  
   //接続を切る
   //$db = null;
    }
    catch(PDOException $e)
    {
     echo $e->getMessage();
     exit;
       $db = null;//接続を切る
    }

?>
<?php
  try
  {
 
   $stmt18 = $db->query("SELECT COUNT(button_id) FROM `answer_table` WHERE button_id = 9 AND flag = 1 AND ball_id = 1 AND user_id = 1");
   $button9_bunsi = $stmt18->fetch(PDO::FETCH_ASSOC);
 
   $button9_seikai = $button9_bunsi['COUNT(button_id)'];

   $db = null;
  }
  catch(PDOException $e)
  {
  echo $e->getMessage();
  exit;
  }
?>
<?php 
  //ユーザー1がbutton1を正解した数 / ユーザー1が解いたbutton1を通過した全問題
  if($button1_tuuka == 0){
    echo $button1_seikai . "/" . $button1_tuuka;
    echo "00";
    echo "%";
  }
  else{
    //echo $button1_seikai . "/" . $button1_tuuka;
    echo "<br />";
    $button1 = $button1_seikai / $button1_tuuka * 100;
    echo ceil($button1);
    echo "%";
  }
  
  
  if($button2_tuuka == 0){
    echo "00";
    echo "%";
  }
  else{
    $button2 = $button2_seikai / $button2_tuuka * 100;
    echo ceil($button2);
    echo "%";
  }
  if($button3_tuuka == 0){
    echo "00";
    echo "%";
  }
  else{
    $button3 = $button3_seikai / $button3_tuuka * 100;
    echo ceil($button3);
    echo "%";
  }
  echo "<br />";
  if($button4_tuuka == 0){
    echo "00";
    echo "%";
  }
  
  else{
    $button4 = $button4_seikai / $button4_tuuka * 100;
    echo ceil($button4);
    echo "%";
  }
  if($button5_tuuka == 0){
    echo "00";
    echo "%";
  }
  else{
    $button5 = $button5_seikai / $button5_tuuka * 100;
    echo ceil($button5);
    echo "%";
  }
  if($button6_tuuka == 0){
    echo "00";
    echo "%";
  }
  else{
    $button6 = $button6_seikai / $button6_tuuka * 100;
    echo ceil($button6);
    echo "%";
  }
  echo "<br />";
  
  if($button7_tuuka == 0){
    echo "00";
    echo "%";
  }
  else{
    $button7 = $button7_seikai / $button7_tuuka * 100;
    echo ceil($button7);
    echo "%";
  }
  if($button8_tuuka == 0){
    echo "00";
    echo "%";
  }
  else{
    $button8 = $button8_seikai / $button8_tuuka * 100;
    echo ceil($button8);
    echo "%";
  }
  if($button9_tuuka == 0){
    echo "00";
    echo "%";
  }
  else{
    $button9 = $button9_seikai / $button9_tuuka * 100;
    echo ceil($button9);
    echo "%";
  }

?>