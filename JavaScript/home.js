
var more;

window.onload = function () {
    var data = location.href.split("?")[1];
    console.log(data);
    var text = data.split("=")[1];
    console.log(text);
    more = text.split("&")[0];
    console.log(more);
}

function receive() {
    location.href = "http://localhost/HTML/index.html?data=" + more;
}

function attack() {
    location.href = "http://localhost/HTML/attack.html?data=" + more;
}