var videoElement;
var frame1 = 0;
var frame2 = 0;
var video_path;
var i = 0;
var x = 0;
var y = 0;
var pop;
var quiet;
var button_id = 0;
var video_id;
var correct;
let judge = 0;
var more;
var most;
var x_coordinate = 0;
var y_coordinate = 0;
var kazu = 0;
var result = 0;
var percentage = 0;
var array = [];
var picture_path;
var hitplace = 0;

function dofy() {
    buttondiv.style.display = "none";
    console.log("dofy()が呼び出されました！！");
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
var color;
var color2;

function getId(ele) {
    console.log("getId(ele)が呼び出されました！！");
    if (stop_renda == 0) {
        button_id = ele.getAttribute("id"); // input要素のid属性の値を取得
        color = document.getElementById(button_id);
        console.log(button_id);
        console.log(color);
        movplay(0);
    }
}


setTimeout(cut, 1);

function cut() {
    console.log("cut()が呼び出されました！！");
    var data = location.href.split("?")[1];
    var text = data.split("=")[1];
    console.log(text);
    more = text.split("&")[0];
    console.log("プレイヤーid :", more);
    most = text.split("&")[1];
    console.log("ボールid :", most);
    // kazu = text.split("|")[1];
    // console.log("解いた問題数：", kazu);
    // result = text.split("|")[2];
    // console.log("正解した数：", result);


    if (kazu == 0) {
        percentage = 0;
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
    back.style.display = "none";
    back_most.style.display = "none";
    $.ajax({
        type: "GET",
        url: "../PHP/index.php",
        dataType: "json",
        data: { 'ball_id': most },
    })
        .done(function (data) {
            var mv = document.getElementById("mv");
            mv.controls = false;
            console.log('DONE', data);
            console.log("通信が成功しました!!!");
            frame1 = data[i]['frame1'];
            frame2 = data[i]['frame2'];
            video_path = data[i]['video_path'];
            video_id = data[i]['video_id'];
            correct = data[i]['ans_id'];
            color2 = document.getElementById(correct);
            picture_path = data[i]['picture_path'];
            console.log("画像のパス:", picture_path);
            x_coordinate = data[i]['x_coordinate'];
            y_coordinate = data[i]['y_coordinate'];
            hitplace = data[i]['hitplace'];
            console.log("x座標：", x_coordinate);
            console.log("y座標：", y_coordinate);
            console.log("打つ場所：", hitplace);
            console.log('frame1　前: ', frame1);
            frame1 = frame1 / 29.97;
            frame1 = frame1 * 1000;
            frame1 = frame1 - 500;
            console.log('frame1　後: ', frame1);
            console.log('DONE', frame2);
            console.log('DONE', video_path);
            console.log('DONE', video_id);
            console.log('正解のボタン番号', correct);
            mv.setAttribute("src", video_path);
            console.log("動画が流れます")
            dofy();
            i = i + 1;
            y = y + 1;
            console.log("カウンター：", i);
            x = data;
            console.log(x);
            console.log(x.length);
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


function wille() {
    console.log("wille()が呼び出されました！！");

    judge = 0;
    color.style.backgroundColor = '#00aeff5b';
    color2.style.backgroundColor = '#00aeff5b';
    percentage = result / kazu * 100;
    console.log("正解率：", percentage);
    percentage = Math.round(percentage);
    console.log("正解率：", percentage);
    total.innerHTML = "ボールの予測地点を選んでください   正解率" + percentage + "％：" + kazu + "問中" + result + "問正解";
    stop_renda = 0;
    if (x.length == i) {
        i = 0
        sent();
    } else {
        console.log(x);
        frame1 = x[i]['frame1'];
        frame2 = x[i]['frame2'];
        video_path = x[i]['video_path'];
        video_id = x[i]['video_id'];
        correct = x[i]['ans_id'];
        x_coordinate = x[i]['x_coordinate'];
        y_coordinate = x[i]['y_coordinate'];
        picture_path = x[i]['picture_path'];
        hitplace = x[i]['hitplace'];
        console.log('frame1　前: ', frame1);
        frame1 = frame1 / 29.97;
        frame1 = frame1 * 1000;
        frame1 = frame1 - 500;
        console.log('frame1　後: ', frame1);
        console.log('DONE', frame2);
        console.log('DONE', video_path);
        console.log('DONE', video_id);
        console.log('正解のボタン', correct);
        color2 = document.getElementById(correct);
        console.log("画像のパス:", picture_path);
        console.log("x座標：", x_coordinate);
        console.log("y座標：", y_coordinate);
        console.log("打つ場所：", hitplace);
        mv.setAttribute("src", video_path);
        i = i + 1;
        y = y + 1;
        console.log("カウンター：", i);
        dofy();
        selectdiv.style.display = "block";
        // console.log("trust :", trust);
    }
}


function apple() {
    if (stop_renda == 0) {
        stop_renda = 1;
        console.log("apple()が呼び出されました！！");
        console.log('frame2　前: ', frame2);
        frame2 = frame2 / 29.97;
        frame2 = frame2 * 1000;
        frame2 = frame2 - 500;
        console.log('frame2　後: ', frame2);
        frame_sa = frame2 - frame1;
        console.log("次止まるまで：", frame_sa);
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
        trust = 0;
        setTimeout(wille, 2000);
        console.log("あってるよ！！！")
        judge = 1;
        result += 1;
        kazu += 1;
        setTimeout(send, 100);

        color.style.backgroundColor = '#00FF0080';
        // color.style.backgroundColor = '#00FF99CC';

        // document.getElementById('maru_sound').play();
    }
    else {
        // setTimeout(out, 2000);
        console.log("まちがってるよ！！！");
        kazu += 1;
        setTimeout(send, 100);
        setTimeout(wille, 2000);
        trust = 0;
        color.style.backgroundColor = '#CD5C5C90';
        color2.style.backgroundColor = '#00FF0080';
        // color2.style.backgroundColor = '#00FF99CC';

        // document.getElementById('batsu_sound').play();
    }
    array.push(
        {
            "ans_id": button_id,
            "hitplace": hitplace,
            "picture_path": picture_path,
            "flag": judge,
        }
    );
    console.log("まとめ:", array);
    buttonobject = document.getElementById("buttonhere");
    link = '<button type="button" class="item" id="' + y + '" onclick="look(this)">' + y + '問目</button>';
    buttonobject.insertAdjacentHTML('beforeend', link);
    judgeobject = document.getElementById("judgehere");
    if (judge == 1) {
        lank = '<button type="button" class="item" id="' + y + '" onclick="look(this)"> ◯ </button>';
    } else {
        lank = '<button type="button" class="item" id="' + y + '" onclick="look(this)">✖</button>';

    }
    judgeobject.insertAdjacentHTML('beforeend', lank);



    // let table = document.getElementById('targetTable');
    // let newRow = table.insertRow();

    // let newCell = newRow.insertCell();
    // let newText = document.createTextNode(y + '問目');
    // newCell.appendChild(newText);

    // newCell = newRow.insertCell();
    // if (judge == 1) {
    //     newText = document.createTextNode('◯');
    // } else {
    //     newText = document.createTextNode('✖');
    // }
    // newCell.appendChild(newText);
}





// function out() {
//     console.log("out()が呼び出されました！！");
//     location.href = "http://localhost/SEN-KEN/HTML/study.html?data=" + more + "|" + correct + "|" + kazu + "|" + result;

// }

function push() {
    location.href = "../HTML/home.html?data=" + more + "&" + most;

}
function pup() {
    front.style.display = "none";
    back.style.display = "block";
    h1.innerHTML = "あなたは<span>" + kazu + "</span>問中<span>" + result + "</span>問正解しました。正解率は<span>" + percentage + "</span>％です。"
}

function send() {
    console.log("send()が呼び出されました！！");
    $.ajax({
        type: "GET",
        url: "../PHP/insert.php",
        dataType: "json",
        data: {
            "ball_id": most,
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

var mam = 0;

function look(ele) {
    console.log("look(ele)が呼び出されました！！");
    mam = -1;
    back_most.style.display = "block";
    // swiperobject = document.getElementById("swiperhere");
    // swiperobject.remove();
    varobject = document.getElementById("var");

    z = ele.getAttribute("id"); // input要素のid属性の値を取得
    z = z - 1;
    console.log(z);
    console.log(array[z]["ans_id"]);
    console.log(array[z]["hitplace"]);
    img_left.setAttribute("src", array[z]["picture_path"]);
    img_left.setAttribute("width", 300);
    img_left.setAttribute("height", 500);

    album = [];
    key1 = array[z]["ans_id"];
    key2 = array[z]["hitplace"];
    console.log("key1 :", key1);
    console.log("key2 :", key2);

    for (let step = 0; step < x.length; step++) {

        if (x[step]['ans_id'] == key1 && x[step]['hitplace'] == key2) {

            album.push(x[step]["picture_path"]);
            console.log(album);
            // links = '<div class="swiper-slide"><img src="' + x[step]["picture_path"] + '" width="400" height="500" alt=""></div>';
            // swiperobject.insertAdjacentHTML('beforeend', links);
            mam = mam + 1;
        }
        varobject.setAttribute("max", mam);
    }
    console.log("mam :", mam);
    // mySwiper = new Swiper('.swiper-container', {
    //     navigation: {
    //         nextEl: '.swiper-button-next',
    //         prevEl: '.swiper-button-prev',
    //     },
    //     loop: true,
    // });
    varobject.addEventListener('input', slide);
    img_right.setAttribute("src", album[0]);
    img_right.setAttribute("width", 300);
    img_right.setAttribute("height", 500);
    // }


}

var da = 0;
function next() {
    da = da + 1;
    if (da > mam) {
        da = 0;
    }
    img_right.setAttribute("src", album[da]);
}

function prev() {
    da = da - 1;
    if (da < 0) {
        da = mam;
    }
    img_right.setAttribute("src", album[da]);
}

function slide() {
    console.log("スライドの値：", varobject.value);
    img_right.setAttribute("src", album[varobject.value]);

}

function ura() {
    for (k = 0; k < 50; k++) {
        buttonobject = document.getElementById("buttonhere");
        link = '<button type="button" class="item" id="' + y + '" onclick="look(this)">' + y + '問目</button>';
        buttonobject.insertAdjacentHTML('beforeend', link);
        judgeobject = document.getElementById("judgehere");
        if (judge == 1) {
            lank = '<button type="button" class="item"> ◯ </button>';
        } else {
            lank = '<button type="button" class="item">✖</button>';

        }
        judgeobject.insertAdjacentHTML('beforeend', lank);

    }
}