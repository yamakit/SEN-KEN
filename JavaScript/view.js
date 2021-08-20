window.onload = function () {
    var data = location.href.split("?")[1];
    var text = data.split("=")[1];
    console.log(text);
    mv.setAttribute("src", text);
    dofy();
}

var all;
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

    videoElement.addEventListener('loadedmetadata', function () {
        all = videoElement.duration;
        console.log(all);

        for (i = 1; i < all + 1; i++) {
            data['labels'].push(i); //1個目のデータセットを追加
            data['datasets'][3]['data'].push(10);
            datas['labels'].push(i); //1個目のデータセットを追加
            datas['datasets'][3]['data'].push(10);
        }
        console.log(datas['labels']);
        ext_chart = new Chart(ctxt, {
            type: 'line',
            data: datas,
            options: options
        });
    });
    videoElement.addEventListener("timeupdate", function () {
        var submit = videoElement.currentTime;
        console.log(submit);
        submit = Math.round(submit);
        console.log(submit);
        data['datasets'][0]['data'].shift();
        data['datasets'][1]['data'].shift();
        data['datasets'][2]['data'].shift();
        datas['datasets'][0]['data'].shift();
        datas['datasets'][1]['data'].shift();
        datas['datasets'][2]['data'].shift();
        // datas['datasets'][0]['data'].pop();
        data['datasets'][0]['data'].push({ x: submit, y: data['datasets'][3]['data'][submit] });
        data['datasets'][1]['data'].push({ x: submit - 1, y: data['datasets'][3]['data'][submit] });
        data['datasets'][2]['data'].push({ x: submit - 2, y: data['datasets'][3]['data'][submit] });
        datas['datasets'][0]['data'].push({ x: submit, y: datas['datasets'][3]['data'][submit] });
        datas['datasets'][1]['data'].push({ x: submit - 1, y: datas['datasets'][3]['data'][submit] });
        datas['datasets'][2]['data'].push({ x: submit - 2, y: datas['datasets'][3]['data'][submit] });
        // console.log(datas['datasets'][1]['data'][submit + 1])
        ex_chart = new Chart(ctx, {
            type: 'line',
            data: data,
            options: option
        });
        ext_chart = new Chart(ctxt, {
            type: 'line',
            data: datas,
            options: options
        });
    })

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
    labels: [],
    datasets: [{
        label: '顔の向き',
        data: [],
        borderColor: 'blue',
        pointBackgroundColor: 'rgba(255, 100, 100, 1)',
        pointRadius: 20,
        lineTension: 0,
        fill: false,
        borderWidth: 3
    },
    {
        label: '顔の向き',
        data: [],
        borderColor: 'blue',
        pointBackgroundColor: 'rgba(255, 100, 100, 0.7)',
        pointRadius: 15,
        lineTension: 0,
        fill: false,
        borderWidth: 3
    },
    {
        label: '顔の向き',
        data: [],
        borderColor: 'blue',
        pointBackgroundColor: 'rgba(255, 100, 100, 0.5)',
        pointRadius: 10,
        lineTension: 0,
        fill: false,
        borderWidth: 3
    },
    {
        label: '顔の向き',
        data: [],
        borderColor: 'pink',
        lineTension: 0,
        fill: false,
        borderWidth: 3
    },
    ]
};

var option = {
    animation: false,
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
    options: option
});




var ctxt = document.getElementById('ext_chart');

var datas = {
    labels: [],
    datasets: [{
        label: '体の開き',
        data: [{}],
        borderColor: 'red',
        // order: 1,
        pointRadius: 20,
        pointBackgroundColor: 'rgba(100, 100, 255, 1)',
        lineTension: 0,
        fill: false,
        borderWidth: 3,
    },
    {
        label: '体の開き',
        data: [{}],
        borderColor: 'red',
        // order: 1,
        pointRadius: 15,
        pointBackgroundColor: 'rgba(100, 100, 255, 0.7)',
        lineTension: 0,
        fill: false,
        borderWidth: 3,
    },
    {
        label: '体の開き',
        data: [{}],
        borderColor: 'red',
        // order: 1,
        pointRadius: 10,
        pointBackgroundColor: 'rgba(100, 100, 255, 0.5)',
        lineTension: 0,
        fill: false,
        borderWidth: 3,
    },
    {
        label: '体の開き',
        data: [],
        borderColor: 'skyblue',
        // order: 3,
        // pointRadius: 20,
        lineTension: 0,
        fill: false,
        borderWidth: 3,
    }],

}

var options = {
    animation: false,
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

