
// function drawVideo() {
//     var video = document.getElementById("mv");
//     // var canvas = document.getElementById("c");
//     // canvas.getContext("2d").drawImage(video, 0, 0, 480, 270);
// }

window.onload = function () {
    var data = location.href.split("?")[1];
    var text = data.split("=")[1];
    console.log(text);
    mv.setAttribute("src", text);
    dofy();
}


function dofy() {
    console.log("dofy()が呼び出されました！！");
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
