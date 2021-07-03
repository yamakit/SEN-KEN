
var more;
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
}

function push() {
    location.href = "http://localhost/HTML/result.html?data=" + more;
}