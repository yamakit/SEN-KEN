
function drawVideo() {
    var video = document.getElementById("mv");
    var canvas = document.getElementById("c");
    canvas.getContext("2d").drawImage(video, 0, 0, 480, 270);
}

window.onload = function () {
    var data = location.href.split("?")[1];
    var text = data.split("=")[1];
    console.log(text);
    mv.setAttribute("src", text);
}