var x;
var y;
videodiv.style.display = "none";
buttondiv.style.display = "none";
// canvas準備
const board = document.querySelector("#board");  //getElementById()等でも可。オブジェクトが取れれば良い。
const ctx = board.getContext("2d");
board.addEventListener("click", (e) => {
    var rect = e.target.getBoundingClientRect()
    x = e.clientX - rect.left
    y = e.clientY - rect.top
    console.log(`${x}:${y}`)
    setTimeout("hikaku()", 100);
});
const chara = new Image();
chara.src = "../valley.png";  // 画像のURLを指定

var zahyo_x;
var zahyo_y;
var path;
var judge = false;
var i = 0;
var f = 0;
array = [];
var counter;
// var number_x;
// var number_y;
var number_r;
var r = [];
var text;

setTimeout("change()", 100);
function change() {

    if (i == 10) {
    }
    else {

        setTimeout("sent()", 100);
    }
}

function sent() {
    $.ajax({
        type: "GET",
        url: "../PHP/attack.php",
        dataType: "json",
        data: { 'yolo_video_table': 0 },
    })
        .done(function (data) {
            console.log('DONE', data);
            console.log("通信が成功しました!!!");
            zahyo_x = data[i]['x_coordinate'];
            zahyo_y = data[i]['y_coordinate'];
            path = data[i]['video_path'];
            console.log('DONE', zahyo_x);
            console.log('DONE', zahyo_y);
            console.log('DONE', path);
            judge = true;
            i = i + 1;
            counter = data;

        }).fail(function (XMLHttpRequest, textStatus, errorThrown) {
            console.log('通信に失敗しました');
            console.log("XMLHttpRequest : " + XMLHttpRequest.status);
            console.log("textStatus     : " + textStatus);
            console.log("errorThrown    : " + errorThrown.message);
        });
}


window.onload = observe();
function observe() {
    if (judge == false) {
        setInterval(observe, 100);
    } else {
        execute();
    }
};

function wille() {

    zahyo_x = counter[i]['x_coordinate'];
    zahyo_y = counter[i]['y_coordinate'];
    path = counter[i]['video_path'];
    console.log('DONE', zahyo_x);
    console.log('DONE', zahyo_y);
    console.log('DONE', path);
    judge = true;
    i = i + 1;
}


function execute() {
    zahyo_x = zahyo_x * 1600;
    zahyo_y = zahyo_y * 1000;
    ctx.drawImage(chara, zahyo_x, zahyo_y, 20, 20);
    judge = false;

    setTimeout("push()", 1);
    setTimeout("wille()", 100);

}

function push() {


    array.push(
        {
            "x": zahyo_x,
            "y": zahyo_y,
            "path": path
        }
    );

    r[f] = Math.sqrt(array[f]["x"] * array[f]["x"] + array[f]["y"] * array[f]["y"]);
    console.log(r[f]);
    f = f + 1;
}

function hikaku() {

    // for (i = 0; i < array.length; i++) {
    //     r[i] = Math.sqrt(array[i]["x"] * array[i]["x"] + array[i]["y"] * array[i]["y"]);
    //     console.log(r[i]);
    // }


    var value = Math.sqrt(x * x + y * y);
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