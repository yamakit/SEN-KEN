var videoElement;
// function drawVideo() {
//     var video = document.getElementById("mv");
//     // var canvas = document.getElementById("c");
//     // canvas.getContext("2d").drawImage(video, 0, 0, 480, 270);
// }

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
    console.log("dofy()が呼び出されました！！");
    buttondiv.style.display = "none";
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


setTimeout(cut, 1);

function cut() {
    console.log("cut()が呼び出されました！！");
    var data = location.href.split("?")[1];
    more = data.split("=")[1];
    console.log("プレイヤーid :", more);
    sent();
}


function sent() {
    console.log("sent()が呼び出されました！！");
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
            console.log('frame1　前: ', frame1);
            frame1 = frame1 / 29.97;
            frame1 = frame1 * 1000;
            // frame1 = frame1 - 1000;
            console.log('frame1　後: ', frame1);
            console.log('DONE', frame2);
            console.log('DONE', video_path);
            console.log('DONE', video_id);
            // console.log('DONE', user_id);
            console.log('正解のボタン番号', correct);
            mv.setAttribute("src", video_path);
            console.log("動画が流れます")
            dofy();
            i = i + 1;
            console.log("カウンター：", i);
            x = data;
            console.log(x);
            a();
        }).fail(function (XMLHttpRequest, textStatus, errorThrown) {
            console.log('通信に失敗しました');
            console.log("XMLHttpRequest : " + XMLHttpRequest.status);
            console.log("textStatus     : " + textStatus);
            console.log("errorThrown    : " + errorThrown.message);
        });
}

var trust = 0;
function a() {
    console.log("a()が呼び出されました！！");

    console.log(frame1);
    videoElement.addEventListener("timeupdate", function () {
        var submit = videoElement.currentTime * 1000;
        // console.log(videoElement.currentTime)
        console.log(frame1 - submit);
        if (frame1 - submit < 2000 && trust == 0) {
            console.log("変わり目");
            selectdiv.style.display = "none";
            videoElement.playbackRate = 1.0;
            var hold = frame1 - submit;
            setTimeout(movplay, hold);
            trust = 1;

            // console.log("trust :", trust);
        }
    });
}
// function change() {
//     console.log("change()が呼び出されました！！");

//     if (i === 4) {
//         location.href = "http://localhost/HTML/result.html?data=" + more + "|" + kazu + "|" + result;
//     }
//     else {
//         trust = 0;
//         // console.log("trust :", trust);
//         setTimeout(wille, 100);
//         // setTimeout(a, 1000);

//     }
// }

function wille() {
    console.log("wille()が呼び出されました！！");
    console.log(x);
    frame1 = x[i]['frame1'];
    frame2 = x[i]['frame2'];
    video_path = x[i]['video_path'];
    video_id = x[i]['video_id'];
    correct = x[i]['ans_id'];
    console.log('frame1　前: ', frame1);
    frame1 = frame1 / 29.97;
    frame1 = frame1 * 1000;
    // frame1 = frame1 - 1000;
    console.log('frame1　後: ', frame1);
    console.log('DONE', frame2);
    console.log('DONE', video_path);
    console.log('DONE', video_id);
    console.log('正解のボタン', correct);
    mv.setAttribute("src", video_path);
    i = i + 1;
    console.log("カウンター：", i);
    dofy();
    selectdiv.style.display = "block";
    // console.log("trust :", trust);
}


function apple() {
    console.log("apple()が呼び出されました！！");
    console.log('frame2　前: ', frame2);
    frame2 = frame2 / 29.97;
    frame2 = frame2 * 1000;
    console.log('frame2　後: ', frame2);
    frame_sa = frame2 - frame1;
    console.log("次止まるまで：", frame_sa);
    // frame2 = 2000;
    setTimeout(movplay, frame_sa);

    quiet = frame_sa;
    quiet = quiet + 1000;
    setTimeout(compare, quiet);
}

function movplay(num) {
    var obj = document.getElementById("mv");
    var n = parseInt(num);
    if (n == 0) {
        obj.play();
    }
    else {
        buttondiv.style.display = "block";
        obj.pause();
    }
}

var kazu = 0;
var result = 0;
function compare() {
    console.log("compare()が呼び出されました！！");
    if (correct === button_id) {
        // setTimeout(change, 2000);
        trust = 0;
        setTimeout(wille, 2000);
        console.log("あってるよ！！！")
        judge = 1;
        result += 1;
        kazu += 1;
        setTimeout(send, 100);

    }
    else {
        setTimeout(out, 2000);
        console.log("まちがってるよ！！！");
        kazu += 1;
        setTimeout(send, 100);
    }
}
function out() {
    console.log("out()が呼び出されました！！");
    // window.location = "../HTML/study.html";
    location.href = "http://localhost/HTML/study.html?data=" + more + "|" + correct + "|" + kazu + "|" + result;

}

function push() {
    location.href = "http://localhost/HTML/result.html?data=" + more + "|" + kazu + "|" + result;
}

function send() {
    console.log("send()が呼び出されました！！");
    $.ajax({
        type: "GET",
        url: "../PHP/insert.php",
        dataType: "json",
        data: {
            "video_id": video_id,
            "button_id": button_id,
            "player_id": more,
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