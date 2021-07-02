
var more;

window.onload = function () {
    var data = location.href.split("?")[1];
    console.log(data);
    var text = data.split("=")[1];
    console.log(text);
    more = text.split("&")[0];
    console.log("プレイヤーid :", more);
}

function push() {
    location.href = "http://localhost/HTML/home.html?data=" + more;
}