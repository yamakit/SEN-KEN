
var more;
var kazu;
var result;
window.onload = function () {
    var data = location.href.split("?")[1];
    console.log(data);
    var text = data.split("=")[1];
    console.log(text);
    more = text.split("|")[0];
    console.log("プレイヤーid :", more);
    most = text.split("|")[1];
    console.log("正解の番号：", most);
    correct.innerHTML = "正解は" + most + "番でした！！！";
    kazu = text.split("|")[2];
    console.log("解いた問題数：", kazu);
    result = text.split("|")[3];
    console.log("正解した数：", result);
}

function push() {
    location.href = "http://localhost/SEN-KEN/HTML/home.html?data=" + more;
}

function back() {
    location.href = "http://localhost/SEN-KEN/HTML/index.html?data=" + more + "|" + kazu + "|" + result;
}