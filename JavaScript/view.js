window.onload = function () {
    var data = location.href.split("?")[1];
    var text = data.split("=")[1];
    console.log(text);
    mv.setAttribute("src", text);
    dofy();
}


function dofy() {
    console.log("dofy()が呼び出されました！！");
    var mv = document.getElementById("mv");
    mv.controls = false;
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
    //     videoElement.playbackRate = 5.0;
    // });

    // btn_veryfast.addEventListener("click", (e) => {
    //     videoElement.playbackRate = 10.0;
    // });

    videoElement.playbackRate = 8.0;

}

buttondiv.style.display = "none";
var i = 0;
function frame() {
    console.log("frame()が呼び出されました。");
    if (i == 0) {
        buttondiv.style.display = "block";
        console.log("ON!");
        i = 1;
    } else {
        buttondiv.style.display = "none";
        console.log("OFF!");
        i = 0;
    }
}

var ctx = document.getElementById("myLineChart");
var myLineChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: [],
        datasets: [
            {
                label: '体の開き',
                data: [33, 1, 37, 1, 34, 5, 8, 25],
                borderColor: "rgba(128,0,0,1)",
                backgroundColor: "rgba(0,0,0,0)"
            },
        ],
    },
    options: {
        title: {
            display: false,
        },
        scales: {
            yAxes: [{
                ticks: {
                    suggestedMax: 100,
                    suggestedMin: 0,
                    stepSize: 5,
                    callback: function (value, index, values) {
                        return value
                    }
                }
            }]
        },
    }
});
