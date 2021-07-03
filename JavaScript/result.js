


var more;
window.onload = function () {
    var data = location.href.split("?")[1];
    console.log(data);
    var text = data.split("=")[1];
    console.log(text);
    more = text.split("|")[0];
    console.log("プレイヤーid :", more);
    most = text.split("|")[1];
    console.log("解いた問題数：", most);
    mostest = text.split("|")[2];
    console.log("正解した数：", mostest);
    // if (most == undefined || mostest == undefined) {
    //     fff.innerHTML = "あなた問題解いてないね！"
    // } else {

    if (most == 0) {
        percentage = 0;
        console.log("こっちだよー");
    } else {
        percentage = mostest / most * 100;
        console.log("正解率：", percentage);
    }
    correct.innerHTML = "あなたは" + most + "問解いて" + mostest + "問正解しました！！";
    percent.innerHTML = "正解率は" + percentage + "％です！！";
}

// }


function push() {
    location.href = "http://localhost/HTML/home.html?data=" + more;
}

function challenge() {
    location.href = "http://localhost/HTML/index.html?data=" + more;
}

