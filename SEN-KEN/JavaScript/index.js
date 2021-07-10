var videoElement;
var frame1 = 0;
var frame2 = 0;
var video_path;
var i = 0;
var x = 0;
var pop;
var quiet;
var button_id = 0;
var video_id;
var correct;
let judge = 0;
var more;
var x_coordinate = 0;
var y_coordinate = 0;
var kazu = 0;
var result = 0;

function dofy() {
    console.log("dofy()が呼び出されました！！");
    buttondiv.style.display = "none";
    marudiv.style.display = "none";
    batsudiv.style.display = "none";
    videoElement = document.querySelector("video");
    const btn_slow = document.getElementById("btn_slow");
    const btn_normal = document.getElementById("btn_normal");
    const btn_fast = document.getElementById("btn_fast");
    const btn_veryfast = document.getElementById("btn_veryfast");

    btn_veryslow.addEventListener("click", (e) => {
        videoElement.playbackRate = 2.0;
    });

    btn_slow.addEventListener("click", (e) => {
        videoElement.playbackRate = 4.0;
    });

    btn_normal.addEventListener("click", (e) => {
        videoElement.playbackRate = 8.0;
    });

    // btn_fast.addEventListener("click", (e) => {
    //     videoElement.playbackRate = 12.0;
    // });

    // btn_veryfast.addEventListener("click", (e) => {
    //     videoElement.playbackRate = 15.0;
    // });
    videoElement.playbackRate = 8.0;

}

var stop_renda = 0;


function getId(ele) {
    if (stop_renda == 0) {
        button_id = ele.getAttribute("id"); // input要素のid属性の値を取得
        console.log(button_id);
    }
}


setTimeout(cut, 1);

function cut() {
    console.log("cut()が呼び出されました！！");
    var data = location.href.split("?")[1];
    var text = data.split("=")[1];
    console.log(text);
    more = text.split("|")[0];
    console.log("プレイヤーid :", more);
    kazu = text.split("|")[1];
    console.log("解いた問題数：", kazu);
    result = text.split("|")[2];
    console.log("正解した数：", result);


    if (kazu == undefined || result == undefined) {
        kazu = 0;
        result = 0;
        percentage = 0;
        // console.log("解いた問題数：", kazu);
        // console.log("正解した数：", result);
    } else {
        kazu = parseInt(kazu);
        result = parseInt(result);
        percentage = result / kazu * 100;
        console.log("正解率：", percentage);
        percentage = Math.round(percentage);
        console.log("正解率：", percentage);
    }

    total.innerHTML = "ボールの予測地点を選んでください   正解率" + percentage + "％：" + kazu + "問中" + result + "問正解";

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
            x_coordinate = data[i]['x_coordinate'];
            y_coordinate = data[i]['y_coordinate'];
            console.log("x座標：", x_coordinate);
            console.log("y座標：", y_coordinate);
            console.log('frame1　前: ', frame1);
            frame1 = frame1 / 29.97;
            frame1 = frame1 * 1000;
            frame1 = frame1 - 500;
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
    percentage = result / kazu * 100;
    console.log("正解率：", percentage);
    percentage = Math.round(percentage);
    console.log("正解率：", percentage);
    total.innerHTML = "ボールの予測地点を選んでください   正解率" + percentage + "％：" + kazu + "問中" + result + "問正解";
    stop_renda = 0;
    console.log(x);
    frame1 = x[i]['frame1'];
    frame2 = x[i]['frame2'];
    video_path = x[i]['video_path'];
    video_id = x[i]['video_id'];
    correct = x[i]['ans_id'];
    x_coordinate = x[i]['x_coordinate'];
    y_coordinate = x[i]['y_coordinate'];
    console.log('frame1　前: ', frame1);
    frame1 = frame1 / 29.97;
    frame1 = frame1 * 1000;
    frame1 = frame1 - 500;
    console.log('frame1　後: ', frame1);
    console.log('DONE', frame2);
    console.log('DONE', video_path);
    console.log('DONE', video_id);
    console.log('正解のボタン', correct);
    console.log("x座標：", x_coordinate);
    console.log("y座標：", y_coordinate);
    mv.setAttribute("src", video_path);
    i = i + 1;
    console.log("カウンター：", i);
    dofy();
    selectdiv.style.display = "block";
    // console.log("trust :", trust);
}


function apple() {
    if (stop_renda == 0) {
        stop_renda = stop_renda + 1;
        console.log("apple()が呼び出されました！！");
        console.log('frame2　前: ', frame2);
        frame2 = frame2 / 29.97;
        frame2 = frame2 * 1000;
        frame2 = frame2 - 500;
        console.log('frame2　後: ', frame2);
        frame_sa = frame2 - frame1;
        console.log("次止まるまで：", frame_sa);
        // frame2 = 2000;
        setTimeout(movplay, frame_sa);

        quiet = frame_sa;
        quiet = quiet + 1000;
        setTimeout(compare, quiet);
    }
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

        button_id.style.backgroundColor = "red";

        marudiv.style.display = "block";
        setTimeout(maru_none, 1000);
        document.getElementById('maru_sound').play();

    }
    else {
        setTimeout(out, 2000);
        console.log("まちがってるよ！！！");
        kazu += 1;
        setTimeout(send, 100);

        batsudiv.style.display = "block";
        setTimeout(batsu_none, 1000);
        document.getElementById('batsu_sound').play();
    }
}

function maru_none() {
    console.log("maru_none()が呼び出されました！！");
    marudiv.style.display = "none";
}

function batsu_none() {
    console.log("batsu_none()が呼び出されました！！");
    batsudiv.style.display = "none";
}



function out() {
    console.log("out()が呼び出されました！！");
    location.href = "http://localhost/SEN-KEN/HTML/study.html?data=" + more + "|" + correct + "|" + kazu + "|" + result;

}

function push() {
    location.href = "http://localhost/SEN-KEN/HTML/home.html?data=" + more;
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
            "user_id": more,
            "judge": judge,
            "x_coordinate": x_coordinate,
            "y_coordinate": y_coordinate,
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





