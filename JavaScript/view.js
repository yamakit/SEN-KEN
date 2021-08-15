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

var ctx = document.getElementById('ex_chart');

var data = {
    labels: ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15"],
    datasets: [{
        label: '顔の向き',
        data: [50, 90, 50, 50, 90, 50, 50, 50, 50, 90, 10, 50, 50, 50, 50],
        borderColor: 'rgba(100, 100, 255, 1)',
        lineTension: 0,
        fill: false,
        borderWidth: 3
    }]
};

var options = {
    scales: {
        xAxes: [{
            scaleLabel: {
                display: true,
                labelString: '秒数'
            }
        }],
        yAxes: [{
            ticks: {
                min: 0,
                max: 100,
                userCallback: function (tick) {
                    return tick.toString();
                }
            },
            scaleLabel: {
                display: true,
                labelString: '左　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　右'
            }
        }]
    },
    title: {
        display: true,
        text: '顔の向きの推移グラフ'
    }
};
var ex_chart = new Chart(ctx, {
    type: 'line',
    data: data,
    options: options
});



var ctxt = document.getElementById('ext_chart');

var datas = {
    labels: ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15"],
    datasets: [{
        label: '体の開き',
        data: [30, 30, 50, 30, 30, 30, 40, 40, 40, 50, 50, 50, 50, 50, 50],
        borderColor: 'rgba(255, 100, 100, 1)',
        lineTension: 0,
        fill: false,
        borderWidth: 3
    }]
};

var options = {
    scales: {
        xAxes: [{
            scaleLabel: {
                display: true,
                labelString: '秒数'
            }
        }],
        yAxes: [{
            ticks: {
                min: 0,
                max: 100,
                userCallback: function (tick) {
                    return tick.toString() + '%';
                }
            },
            scaleLabel: {
                display: true,
                labelString: '閉　　　　　　　　　　　　　　　　　　　　　　　　　開'
            }
        }]
    },
    title: {
        display: true,
        text: '体の開き'
    }
};
var ext_chart = new Chart(ctxt, {
    type: 'line',
    data: datas,
    options: options
});