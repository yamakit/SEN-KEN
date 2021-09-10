<?php

if(!empty($_GET)){
    $name = $_GET['name'];
    $affiliation = $_GET['club'];
    $position = $_GET['free'];
    $roma = $_GET['roma'];
    // $face_image = $_FILES['upimg']['name'];
    // move_uploaded_file($_FILES['upimg']['tmp_name'], './upload/' . $face_image);
    // echo '<img src="img.php?img_name=' . $face_image . '">';

    if( !empty($_FILES['upimg']['tmp_name']) && is_uploaded_file($_FILES['upimg']['tmp_name']) ) {

        // ファイルを指定したパスへ保存する
        if( move_uploaded_file( $_FILES['upimg']['tmp_name'], $path.'../img/'.$roma.'.jpg') ) {
            echo 'アップロードされたファイルを保存しました。';
        } else {
            echo 'アップロードされたファイルの保存に失敗しました。';
        }
    }
        // echo $path;



    if($affiliation == "バレーボール"){
        $ball_id = 1;
        }else if($affiliation == "バドミントン"){
        $ball_id = 2;
        }else{
        $ball_id = 3;
    }

$dsn = 'mysql:dbname=sen-ken;host=localhost';
$user = 'root';
$password = '';
$result = array();

try {
    $dbh = new PDO($dsn, $user, $password);  


    $sql = "INSERT INTO `users`(`ball_id`, `name`, `affiliation`, `position`, `face_image`) VALUES ($ball_id, '$name', '$affiliation', '$position', 1)";
    $dbh -> query($sql);
    $id = $dbh -> lastInsertId();
    echo $id;

} catch (Exception $e) {
echo $e->getMessage();
exit();
}

}

header("Location:../HTML/home.html?SelectPref=".$id."=&submit");
?>