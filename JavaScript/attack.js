var x;
var y;
const board = document.querySelector("#board");  //getElementById()等でも可。オブジェクトが取れれば良い。
const ctx = board.getContext("2d");
board.addEventListener("click", (e) => {
    var rect = e.target.getBoundingClientRect()
    x = e.clientX - rect.left
    y = e.clientY - rect.top
    console.log(`${x}:${y}`)
    setTimeout(hikaku, 100);
});
const chara = new Image();
chara.src = "../valley.png";  // 画像のURLを指定

var zahyo_x;
var zahyo_y;
var path;
var judge = false;
var array = [];
var counter;
// var number_x;
// var number_y;
var number_r;
var r = [];
var text;
var more;

setTimeout(cut, 1);

function cut() {
    var data = location.href.split("?")[1];
    more = data.split("=")[1];
    console.log("プレイヤーid :", more);
    sent();
}

// setTimeout(sent, 500);
function sent() {
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
            // zahyo_x = data[i]['x_coordinate'];
            // zahyo_y = data[i]['y_coordinate'];
            // path = data[i]['video_path'];
            // console.log('DONE', zahyo_x);
            // console.log('DONE', zahyo_y);
            // console.log('DONE', path);
            // judge = true;
            // i = i + 1;
        }).fail(function (XMLHttpRequest, textStatus, errorThrown) {
            console.log('通信に失敗しました');
            console.log("XMLHttpRequest : " + XMLHttpRequest.status);
            console.log("textStatus     : " + textStatus);
            console.log("errorThrown    : " + errorThrown.message);
        });

}


function push() {

    for (i = 0; i < 4; i++) {
        zahyo_x = counter[i]['x_coordinate'];
        zahyo_y = counter[i]['y_coordinate'];
        path = counter[i]['video_path'];
        console.log(zahyo_x);
        console.log(zahyo_y);
        console.log(path);

        zahyo_x = zahyo_x * 1600;
        zahyo_y = zahyo_y * 1000;
        ctx.drawImage(chara, zahyo_x, zahyo_y, 20, 20);


        array.push(
            {
                "x": zahyo_x,
                "y": zahyo_y,
                "path": path
            }
        );

        r[i] = Math.sqrt(array[i]["x"] * array[i]["x"] + array[i]["y"] * array[i]["y"]);
        console.log(r[i]);
    }
}

function hikaku() {

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
    console.log(array[number_r]["path"]);
    location.href = "http://localhost/HTML/view.html?data=" + text;
    // if (number_r) {
    // mv.setAttribute("src", array[number_r]["path"]);
    // plotdiv.style.display = "none";
    // videodiv.style.display = "block";
    // buttondiv.style.display = "block";

    // } else {
    //     console.log("これじゃあ動画は再生できないね！！")
    // }


}

// function push() {
//     location.href = "http://localhost/HTML/home.html?data=" + more;
// }


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