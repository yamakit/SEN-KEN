var x;
var y;
// canvas準備
const board = document.querySelector("#board");
const ctx = board.getContext("2d");
board.addEventListener("click", (e) => {  //クリックしたマウス座標を取得
    var rect = e.target.getBoundingClientRect()
    x = e.clientX - rect.left
    y = e.clientY - rect.top
    console.log(`${x}:${y}`)
    setTimeout(hikaku, 100);
});
const chara = new Image();


var zahyo_x;
var zahyo_y;
var path;
var judge = false;
var array = [];
var counter;
var hitplace;
// var number_x;
// var number_y;
var number_r;
var r = [];
var text;
var more;
var most;
var add;
setTimeout(cut, 1);

function cut() {　// リンクからプレイヤーidとボールidを取得
    var data = location.href.split("?")[1];
    text = data.split("=")[1];
    console.log(text);
    more = text.split("&")[0];
    console.log("プレイヤーid :", more);
    most = text.split("&")[1];
    console.log("ボールid :", most);
    if (most == 1) {
        chara.src = "../img/volley.png";  // 画像のURLを指定
    } else if (most == 2) {
        chara.src = "../img/bad.png"
    }
    sent();
}


function sent() {　//データベースからデータを取得
    console.log("sent()が呼び出されました！！");
    $.ajax({
        type: "GET",
        url: "../PHP/attack.php",
        dataType: "json",
        data: { 'player_id': more },
    })
        .done(function (data) {
            console.log('DONE', data);
            console.log("通信が成功しました!!!");
            counter = data;
            push();

        }).fail(function (XMLHttpRequest, textStatus, errorThrown) {
            console.log('通信に失敗しました');
            console.log("XMLHttpRequest : " + XMLHttpRequest.status);
            console.log("textStatus     : " + textStatus);
            console.log("errorThrown    : " + errorThrown.message);
        });

}


function push() {　//バレーボールの画像をプロット

    for (i = 0; i < counter.length; i++) {
        zahyo_x = counter[i]['x_coordinate'];
        zahyo_y = counter[i]['y_coordinate'];
        path = counter[i]['video_path'];
        hitplace = counter[i][`hitplace`];
        console.log(zahyo_x);
        console.log(zahyo_y);
        console.log(path);
        console.log(hitplace);

        zahyo_x = zahyo_x * 1600;
        zahyo_y = zahyo_y * 1000;
        ctx.drawImage(chara, zahyo_x, zahyo_y, 30, 40);
        // ctx.beginPath();

        // ctx.arc(zahyo_x, zahyo_y, 15, 0, Math.PI * 2, false);
        // ctx.fillStyle = "rgba(0,0,0,0.3)"; //青で不透明度0.3で塗り潰す
        // ctx.fill();


        array.push(
            {
                "x": zahyo_x,
                "y": zahyo_y,
                "path": path,
                "hitplace": hitplace,
            }
        );

        r[i] = Math.sqrt(array[i]["x"] * array[i]["x"] + array[i]["y"] * array[i]["y"]);
        console.log(r[i]);
    }
}

function hikaku() {　//マウス座標から一番近い画像を検索、その画像の動画を再生

    var value = Math.sqrt(x * x + y * y);
    console.log(value);
    var diff = [];
    var index = 0;
    i = 0;
    $(r).each(function (i, val) {
        diff[i] = Math.abs(value - val);
        // console.log(value);
        // console.log(val);
        // console.log(diff[i]);
        index = (diff[index] < diff[i]) ? index : i;
    });
    console.log(diff);
    console.log(index);
    number_r = index;

    text = array[number_r]["path"];
    console.log(text);
    add = array[number_r]["hitplace"];
    console.log(add);
    location.href = "../HTML/view.html?data=" + text + "&" + more + "&" + add;
}



// var text = document.getElementById("sendText").value;

// function plot() {
//     plotdiv.style.display = "block";
//     videodiv.style.display = "none";

// }
// i = 0;
// console.log(array);
// var value = x;
// var diff = [];
// var index = 0;
// $(array).each(function (i, val) {
//     diff[i] = Math.abs(value - val["x"]);
//     console.log(value);
//     console.log(val["x"]);
//     console.log(diff[i]);
//     index = (diff[index] < diff[i]) ? index : i;
// });
// console.log(arr1);
// console.log(array[index]);
// console.log(diff);
// number_x = index;

// i = 0;
// value = y;
// diff = [];
// index = 0;
// $(array).each(function (i, val) {
//     diff[i] = Math.abs(value - val["y"]);
//     console.log(value);
//     console.log(val["y"]);
//     console.log(diff[i]);
//     index = (diff[index] < diff[i]) ? index : i;
// });
// console.log(array[index]);
// console.log(diff);
// number_y = index;

