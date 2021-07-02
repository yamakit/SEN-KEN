var videoElement;
function drawVideo() {
    var video = document.getElementById("mv");
    var canvas = document.getElementById("c");
    canvas.getContext("2d").drawImage(video, 0, 0, 480, 270);
}

var frame1 = 0;
var frame2 = 0;
var video_path;
var i = 0;
var x = 0;
var pop;
var quiet;
// var user_id;
var button_id = 0;
var video_id;
var correct;
let judge = 0;
var more;
var nowTime;

function dofy() {

    videoElement = document.querySelector("video");
    const btn_slow = document.getElementById("btn_slow");
    const btn_normal = document.getElementById("btn_normal");
    const btn_fast = document.getElementById("btn_fast");
    const btn_veryfast = document.getElementById("btn_veryfast");

    btn_slow.addEventListener("click", (e) => {
        videoElement.playbackRate = 0.5;
    });

    btn_normal.addEventListener("click", (e) => {
        videoElement.playbackRate = 1.0;
    });

    btn_fast.addEventListener("click", (e) => {
        videoElement.playbackRate = 5.0;
    });

    btn_veryfast.addEventListener("click", (e) => {
        videoElement.playbackRate = 10.0;
    });

}



function getId(ele) {
    button_id = ele.getAttribute("id"); // input要素のid属性の値を取得
    console.log(button_id);
}


setTimeout(cut(), 1);

function cut() {
    var data = location.href.split("?")[1];
    more = data.split("=")[1];
    console.log(more);
}

setTimeout(sent(), 100);
function sent() {
    $.ajax({
        type: "GET",
        url: "../PHP/index.php",
        dataType: "json",
        data: { 'yolo_video_table': 0 },
    })
        .done(function (data) {
            var mv = document.getElementById("mv");
            console.log('DONE', data);
            console.log("通信が成功しました!!!");
            frame1 = data[i]['frame1'];
            frame2 = data[i]['frame2'];
            video_path = data[i]['video_path'];
            video_id = data[i]['video_id'];
            // user_id = data[i]['player_id'];
            correct = data[i]['ans_id'];
            console.log('DONE', frame1);
            frame1 = frame1 / 29.97;
            frame1 = frame1 * 1000;
            frame1 = frame1 - 1000;
            console.log('DONE', frame2);
            console.log('DONE', video_path);
            console.log('DONE', video_id);
            // console.log('DONE', user_id);
            console.log('正解のボタン番号', correct);
            mv.setAttribute("src", video_path);
            dofy();
            i = i + 1;
            console.log(i);
            x = data;
            console.log(x);
        }).fail(function (XMLHttpRequest, textStatus, errorThrown) {
            console.log('通信に失敗しました');
            console.log("XMLHttpRequest : " + XMLHttpRequest.status);
            console.log("textStatus     : " + textStatus);
            console.log("errorThrown    : " + errorThrown.message);
        });
}

setTimeout("a()", 1000);


// function view() {
//     frame1 = frame1 / 29.97;
//     frame1 = frame1 * 1000;
//     frame1 = frame1 - 1000;
//     console.log(frame1);
//     setTimeout(movplay, frame1);
// }

var trust = 0;
function a() {
    console.log("a()が呼び出されました！！");

    console.log(frame1);
    videoElement.addEventListener("timeupdate", function () {
        var submit = videoElement.currentTime * 1000;
        // console.log(videoElement.currentTime)
        console.log(frame1 - submit);
        if (frame1 - submit < 3000 && trust == 0) {
            selectdiv.style.display = "none";
            videoElement.playbackRate = 1.0;
            var hold = frame1 - submit;
            setTimeout("movplay()", hold);
            // console.log("セットタイムアウト呼び出しまで" + hold);
            trust = 1;
            console.log("trust :", trust);
        }
    });
}
function change() {

    if (i === 10) {
        window.location = "../HTML/home.html";
    }
    else {
        trust = 0;
        setTimeout("wille()", 100);
        setTimeout("a()", 1000);

    }
}

function wille() {

    console.log(x);
    frame1 = x[i]['frame1'];
    frame2 = x[i]['frame2'];
    video_path = x[i]['video_path'];
    video_id = x[i]['video_id'];
    correct = x[i]['ans_id'];
    console.log('frame1　前: ', frame1);
    frame1 = frame1 / 29.97;
    frame1 = frame1 * 1000;
    frame1 = frame1 - 1000;
    console.log('frame1　後: ', frame1);
    console.log('DONE', frame2);
    console.log('DONE', video_path);
    console.log('DONE', video_id);
    console.log('正解のボタン', correct);
    mv.setAttribute("src", video_path);
    i = i + 1;
    console.log(i);
    dofy();
    selectdiv.style.display = "block";
    console.log("trust :", trust);
}


function apple() {
    // frame2 = frame2 / 29.97;
    // frame2 = frame2 * 1000;
    // console.log(frame2);
    frame2 = 2000;
    setTimeout("movplay()", frame2);
    // pop = frame2;
    // pop = pop + 3000;

    quiet = frame2;
    quiet = quiet + 1000;
    // setTimeout("change()", pop);
    setTimeout("compare()", quiet);
}

function movplay(num) {
    var obj = document.getElementById("mv");
    var n = parseInt(num);
    if (n == 0) {
        obj.play();
    }
    else {
        obj.pause();
    }
}

function compare() {
    if (correct === button_id) {
        setTimeout("change()", 2000);
        console.log("あってるよ！！！")
        judge = 1;
        setTimeout("send()", 100);

    }
    else {
        setTimeout("out()", 2000)
        console.log("まちがってるよ！！！");
        setTimeout("send()", 100);
    }
}
function out() {
    window.location = "../HTML/study.html";
}

function send() {
    $.ajax({
        type: "GET",
        url: "../PHP/insert.php",
        dataType: "json",
        data: {
            "video_id": video_id,
            "button_id": button_id,
            "user_id": more,
            "judge": judge
        },
    })
        .done(function (data) {
            console.log('通信に成功しました', data);
        }).fail(function (XMLHttpRequest, textStatus, errorThrown) {
            console.log('通信に失敗しました');
            console.log("XMLHttpRequest : " + XMLHttpRequest.status);
            console.log("textStatus     : " + textStatus);
            console.log("errorThrown    : " + errorThrown.message);
        });
}