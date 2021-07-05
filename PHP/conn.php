<?php
//header("Content-Type: application/json; charset=utf-8");
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
//プルダウンの選択を受け取る
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

$button_cnt = 9;
# [1..$button_cnt]の整数の配列を生成し、それに対してMapを仕掛ける
# =ボタンの数だけの要素数を持つ配列をつくれる
$result = array_map(function($num) use ($user_filtered) {
    // お目当てのボタンIDのデータのみ抽出
    $button_filtered = array_filter($user_filtered, function($x) use ($num) {
        $button_id = $num;
        return $x['button_id'] == $button_id;
    });
    // 解いた問題数が0でない場合連想配列に入れる
    if ($button_filtered) {
        // 正解したデータを抽出
        $correct_filtered = array_filter($button_filtered, function($x) {
            return $x['judge'] == 1;
        });
        // 上から解いた問題数、正解数、正答率
        $question_cnt = count($button_filtered);
        $correct_cnt = count($correct_filtered);
        $correct_rate = floor(($correct_cnt / $question_cnt) * 100);

        # 連想配列を返却 -> $resultの一要素になる
        return [
            'question_count' => $question_cnt,
            'correct_count' => $correct_cnt,
            'correct_rate' => $correct_rate
        ];
    } else {
        # 解いた問題がなければ全データ0の連想配列を返却
        return [
            'question_count' => 0,
            'correct_count' => 0,
            'correct_rate' => 0
        ];
    }
}, range(1, $button_cnt));
//$result内の連想配列をjsonencodeする
header('Content-type: application/json');
$json = json_encode($result,JSON_UNESCAPED_UNICODE);
echo json_encode($result,JSON_UNESCAPED_UNICODE);
<<<<<<< HEAD
?>

=======
?>
>>>>>>> demo
