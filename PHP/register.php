<?php

if(!empty($_POST)){
    $name = $_POST['name'];
    $affiliation = $_POST['club'];
    $position = $_POST['free'];
    $face_image = "../img/" . $_FILES['upimg']['name'];
    
    if(!empty($_FILES['upimg']['tmp_name']) && is_uploaded_file($_FILES['upimg']['tmp_name']) ) {

        // ファイルを指定したパスへ保存する
        if( move_uploaded_file( $_FILES['upimg']['tmp_name'], $face_image) ) {
            echo 'アップロードされたファイルを保存しました。';
        } else {
            echo 'アップロードされたファイルの保存に失敗しました。';
        }
    }



    if($affiliation == "バレーボール"){
        $ball_id = 1;
        }else if($affiliation == "バドミントン"){
        $ball_id = 2;
        }

$dsn = 'mysql:dbname=sen-ken;host=localhost';
$user = 'root';
$password = '';
$result = array();

try {
    $dbh = new PDO($dsn, $user, $password);  

    // データベースへ名前、ball_idなどの値をインサート
    $sql = "INSERT INTO `users`(`ball_id`, `name`, `affiliation`, `position`, `face_image`) VALUES ($ball_id, '$name', '$affiliation', '$position', '$face_image')";
    $dbh -> query($sql);
    $id = $dbh -> lastInsertId();
    echo $id;

} catch (Exception $e) {
echo $e->getMessage();
exit();
}

}

header("Location:../HTML/home.html?SelectPref=".$id."&".$ball_id);

?>