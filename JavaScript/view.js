var more;
var most;
var text;
var da;
window.onload = function () {   //リンクから動画のsrc、プレイヤーid、打つ場所を取得
    var data = location.href.split("?")[1];
    var a = data.split("=")[1];
    console.log(a);
    text = a.split("&")[0];
    console.log("動画のパス :", text);
    mv.setAttribute("src", text);
    more = a.split("&")[1];
    console.log("プレイヤーid :", more);
    most = a.split("&")[2];
    console.log("打つ場所 :", most);
    dofy();
    send();
    graph();
}


var all;
var submit;
function dofy() {　//動画の再生速度を変更、動画の現在の秒数を取得しグラフに描画
    console.log("dofy()が呼び出されました！！");
    var mv = document.getElementById("mv");
    mv.controls = false;
    videoElement = document.querySelector("video");
    const btn_veryslow = document.getElementById("btn_veryslow");
    const btn_slow = document.getElementById("btn_slow");
    const btn_normal = document.getElementById("btn_normal");
    const stop = document.getElementById("stop");
    // const btn_veryfast = document.getElementById("btn_veryfast");

    btn_veryslow.addEventListener("click", (e) => {
        videoElement.playbackRate = 2.0;
    });

    btn_slow.addEventListener("click", (e) => {
        videoElement.playbackRate = 4.0;
    });

    btn_normal.addEventListener("click", (e) => {
        videoElement.playbackRate = 8.0;
    });


    videoElement.playbackRate = 8.0;


    //     videoElement.addEventListener('loadedmetadata', function () {
    //         all = videoElement.duration;
    //         console.log(all);

    //         // for (i = 1; i < all + 1; i++) {
    //         //     // data['labels'].push(i); //1個目のデータセットを追加
    //         //     // data['datasets'][3]['data'].push(10);
    //         //     datas['labels'].push(i); //1個目のデータセットを追加
    //         //     // datas['datasets'][3]['data'].push(10);
    //         // }
    //         // console.log(datas['labels']);
    //         ext_chart = new Chart(ctxt, {
    //             type: 'line',
    //             data: datas,
    //             options: options
    //         });
    //     });
    videoElement.addEventListener("timeupdate", function () {
        submit = videoElement.currentTime;
        // submit = submit * 29.97;
        // console.log(submit);
        submit = Math.round(submit);
        console.log(submit);
        // let Day = new Date();
        // console.log(Day.getMilliseconds());
        datass['datasets'][0]['data'].shift();
        // datass['datasets'][1]['data'].shift();
        // datass['datasets'][2]['data'].shift();
        datas['datasets'][0]['data'].shift();
        // datas['datasets'][1]['data'].shift();
        // datas['datasets'][2]['data'].shift();
        // datas['datasets'][0]['data'].pop();
        datass['datasets'][0]['data'].push({ x: submit, y: datass['datasets'][1]['data'][submit - 1] });
        // datass['datasets'][1]['data'].push({ x: submit - 1, y: data['datasets'][3]['data'][submit] });
        // datass['datasets'][2]['data'].push({ x: submit - 2, y: data['datasets'][3]['data'][submit] });
        datas['datasets'][0]['data'].push({ x: submit, y: datas['datasets'][1]['data'][submit - 1] });
        // datas['datasets'][1]['data'].push({ x: submit - 1, y: datas['datasets'][3]['data'][submit - 1] });
        // datas['datasets'][2]['data'].push({ x: submit - 2, y: datas['datasets'][3]['data'][submit - 2] });
        // console.log(datas['datasets'][1]['data'][submit + 1])
        ex_chart = new Chart(ctx, {
            type: 'line',
            data: datass,
            options: option
        });
        ext_chart = new Chart(ctxt, {
            type: 'line',
            data: datas,
            options: options
        });

    })

}



//     // ext_chart = new Chart(ctxt, {
//     //     type: 'line',
//     //     data: datas,
//     //     options: options
//     //     });
// }


buttondiv.style.display = "none";
var rr = 0;
function frame() {　//動画の枠のON、OFFの切り替え
    console.log("frame()が呼び出されました。");
    if (rr == 0) {
        buttondiv.style.display = "block";
        console.log("ON!");
        rr = 1;
    } else {
        buttondiv.style.display = "none";
        console.log("OFF!");
        rr = 0;
    }
}

back.style.display = "none";
function a() {　//体の開きのグラフ、顔の向きのグラフの表示の切り替え
    console.log("a()が呼び出されました。")
    checkValue = '';
    let Radio = document.getElementsByName('tab_name');

    for (let u = 0; u < Radio.length; u++) {
        if (Radio.item(u).checked) {
            checkValue = Radio.item(u).value;
        }
        console.log("checkk", checkValue);
        if (checkValue == 0) {
            front.style.display = "block";
            back.style.display = "none";
        } else if (checkValue == 1) {
            front.style.display = "none";
            back.style.display = "block";
        }
    }
}

var ctx = document.getElementById('myChart01');
// ctx.style.backgroundColor = "#EEEEEE";
var datass = {
    labels: [],
    datasets: [{
        label: '現在の動画の体の開き',
        data: [],
        borderColor: '#0033FF80',
        pointBackgroundColor: '#0033FF80',
        pointRadius: 7,
        lineTension: 0,
        fill: false,
        borderWidth: 3
    },
    // {
    //     label: '体の開き',
    //     data: [],
    //     borderColor: 'blue',
    //     pointBackgroundColor: 'rgba(255, 100, 100, 0.7)',
    //     pointRadius: 15,
    //     lineTension: 0,
    //     fill: false,
    //     borderWidth: 3
    // },
    // {
    //     label: '体の開き',
    //     data: [],
    //     borderColor: 'blue',
    //     pointBackgroundColor: 'rgba(255, 100, 100, 0.5)',
    //     pointRadius: 10,
    //     lineTension: 0,
    //     fill: false,
    //     borderWidth: 3
    // },
    {
        label: '体の開き',
        data: [],
        borderColor: '#ff000080',
        pointRadius: 0.1,
        lineTension: 0,
        fill: false,
        borderWidth: 3
    },
    ]
};


var option = {
    animation: false,
    // events: [],
    scales: {
        xAxes: [{
            ticks: {
                maxTicksLimit: 10
            },
            scaleLabel: {
                display: true,
                labelString: '秒数'
            }
        }],
        yAxes: [{
            ticks: {
                min: -100,
                max: 100,
                stepSize: 20,
                fontSize: 10,
                userCallback: function (tick) {
                    return tick.toString() + '%';
                }
            },
            scaleLabel: {
                display: true,
                labelString: '閉　　　　　　　　　　　　　　　　　開'
            }
        }]
    },
    title: {
        display: true,
        // text: '体の開きの推移グラフ'
        text: '',
        fontSize: 16,
    }
};
var ex_chart = new Chart(ctx, {
    type: 'line',
    data: datass,
    options: option
});




var ctxt = document.getElementById('myChart02');
// ctxt.style.backgroundColor = "#E9E9E9";
var datas = {
    labels: [],
    datasets: [{
        label: '現在の動画の顔の向き',
        data: [{}],
        borderColor: '#ff000080',
        // order: 1,
        pointRadius: 7,
        pointBackgroundColor: '#ff000080',
        lineTension: 0,
        fill: false,
        borderWidth: 3,
    },
    // {
    //     label: '顔の向き',
    //     data: [{}],
    //     borderColor: 'red',
    //     // order: 1,
    //     pointRadius: 15,
    //     pointBackgroundColor: 'rgba(100, 100, 255, 0.7)',
    //     lineTension: 0,
    //     fill: false,
    //     borderWidth: 3,
    // },
    // {
    //     label: '顔の向き',
    //     data: [{}],
    //     borderColor: 'red',
    //     // order: 1,
    //     pointRadius: 10,
    //     pointBackgroundColor: 'rgba(100, 100, 255, 0.5)',
    //     lineTension: 0,
    //     fill: false,
    //     borderWidth: 3,
    // },
    {
        label: '顔の向き',
        data: [],
        borderColor: '#0033FF80',
        // order: 3,
        pointRadius: 0.1,
        lineTension: 0,
        fill: false,
        borderWidth: 3,
    }],

}

var options = {
    animation: false,
    // events: [],
    scales: {
        xAxes: [{
            ticks: {
                maxTicksLimit: 10
            },
            scaleLabel: {
                display: true,
                labelString: '秒数'
            }
        }],
        yAxes: [{
            ticks: {
                min: -100,
                max: 100,
                stepSize: 20,
                fontSize: 10,
                userCallback: function (tick) {
                    return tick.toString() + '%';
                }
            },
            scaleLabel: {
                display: true,
                labelString: '左　　　　　　　　　　　　　　　　　　右'
            }
        }]
    },
    title: {
        display: true,
        // text: '顔の向きの推移グラフ'
        text: '',
        fontSize: 16,
    }
};
var ext_chart = new Chart(ctxt, {
    type: 'line',
    data: datas,
    options: options
});

var n = 1;
function mov() {　//動画の再生と停止の切り替え
    var obj = document.getElementById("mv");
    if (n == 0) {
        obj.play();
        n = 1;
    }
    else {
        obj.pause();
        n = 0;
    }
}


function send() {　　　　//データベースからデータを取得、表に数字を表示
    console.log("send()が呼び出されました！！");
    $.ajax({
        type: "GET",
        url: "../PHP/view.php",
        dataType: "json",
        data: {
            'player_id': more,
            'hitplace': most,
        },
    })
        .done(function (data) {
            console.log('DONE', data);
            console.log("通信が成功しました!!!");
            ann.innerHTML = "直近" + data.length + "本打ったコース別の累積";
            button1 = 0;
            button2 = 0;
            button3 = 0;
            button4 = 0;
            button5 = 0;
            button6 = 0;
            button7 = 0;
            button8 = 0;
            button9 = 0;
            // console.log(data[2][0]);
            for (i = 0; i < data.length; i++) {
                if (data[i]['ans_id'] == 1) {
                    button1 += 1;
                } else if (data[i]['ans_id'] == 2) {
                    button2 += 1;
                } else if (data[i]['ans_id'] == 3) {
                    button3 += 1;
                } else if (data[i]['ans_id'] == 4) {
                    button4 += 1;
                } else if (data[i]['ans_id'] == 5) {
                    button5 += 1;
                } else if (data[i]['ans_id'] == 6) {
                    button6 += 1;
                } else if (data[i]['ans_id'] == 7) {
                    button7 += 1;
                } else if (data[i]['ans_id'] == 8) {
                    button8 += 1;
                } else if (data[i]['ans_id'] == 9) {
                    button9 += 1;
                }

            }
            if (data.length == 0) {
                percentage1 = 0;
                percentage2 = 0;
                percentage3 = 0;
                percentage4 = 0;
                percentage5 = 0;
                percentage6 = 0;
                percentage7 = 0;
                percentage8 = 0;
                percentage9 = 0;
            } else {
                percentage1 = Math.round(button1 / data.length * 100);
                percentage2 = Math.round(button2 / data.length * 100);
                percentage3 = Math.round(button3 / data.length * 100);
                percentage4 = Math.round(button4 / data.length * 100);
                percentage5 = Math.round(button5 / data.length * 100);
                percentage6 = Math.round(button6 / data.length * 100);
                percentage7 = Math.round(button7 / data.length * 100);
                percentage8 = Math.round(button8 / data.length * 100);
                percentage9 = Math.round(button9 / data.length * 100);
            }

            color1 = document.getElementById("td1");
            color2 = document.getElementById("td2");
            color3 = document.getElementById("td3");
            color4 = document.getElementById("td4");
            color5 = document.getElementById("td5");
            color6 = document.getElementById("td6");
            color7 = document.getElementById("td7");
            color8 = document.getElementById("td8");
            color9 = document.getElementById("td9");
            var tdArray = [color1, color2, color3, color4, color5, color6, color7, color8, color9];

            color1.innerHTML = button1 + "本\n" + percentage1 + "%";
            color2.innerHTML = button2 + "本\n" + percentage2 + "%";
            color3.innerHTML = button3 + "本\n" + percentage3 + "%";
            color4.innerHTML = button4 + "本\n" + percentage4 + "%";
            color5.innerHTML = button5 + "本\n" + percentage5 + "%";
            color6.innerHTML = button6 + "本\n" + percentage6 + "%";
            color7.innerHTML = button7 + "本\n" + percentage7 + "%";
            color8.innerHTML = button8 + "本\n" + percentage8 + "%";
            color9.innerHTML = button9 + "本\n" + percentage9 + "%";


            var percentageArray = [percentage1, percentage2, percentage3, percentage4, percentage5, percentage6, percentage7, percentage8, percentage9];
            var orderArray = [percentage1, percentage2, percentage3, percentage4, percentage5, percentage6, percentage7, percentage8, percentage9];
            console.log(orderArray);
            c1 = '#ff000080';
            c2 = '#ffff0080';
            c3 = '#0033FF80';
            var y = 0;
            var z = 0;
            var colorArray = [c3, c2, c1];
            percentageArray.sort(function (a, b) { return (b - a); });
            console.log(percentageArray);
            for (i = 0; i < percentageArray.length; i++) {
                var search = orderArray.indexOf(percentageArray[i]);
                console.log(search);
                if (y == 0) {
                    if (i < 3) {
                        z = 0;
                    } else if (i < 6) {
                        z = 1;
                    } else {
                        z = 2;
                    }
                    tdArray[search].style.backgroundColor = colorArray[z];
                    console.log(search + 1, "のパネルが変えられたよ");
                    orderArray[search] = 1000;
                    console.log(orderArray);
                    var search2 = orderArray.indexOf(percentageArray[i]);
                    console.log(search2);
                    if (percentageArray[i] == 0) {
                        console.log("00000000000000000000000");
                        tdArray[search].style.backgroundColor = colorArray[2];
                    } else if (search2 == -1) {
                    } else {
                        tdArray[search2].style.backgroundColor = colorArray[z];
                        // orderArray[search2] = 1000;
                        console.log(search2 + 1, "のパネルが変えられたよ -- search2");
                        y = 1;
                    }
                } else {
                    y = 0;
                }


            }



        }).fail(function (XMLHttpRequest, textStatus, errorThrown) {
            console.log('通信に失敗しました');
            console.log("XMLHttpRequest : " + XMLHttpRequest.status);
            console.log("textStatus     : " + textStatus);
            console.log("errorThrown    : " + errorThrown.message);
        });

}

function graph() {　//データベースから顔の向きのデータを取得、グラフに描画
    console.log("graph()が呼び出されました！！");
    $.ajax({
        type: "GET",
        url: "../PHP/view2.php",
        dataType: "json",
        data: {
            'path': text,
        },
    })
        .done(function (data) {
            console.log('DONE', data);
            console.log("通信が成功しました!!!");
            // console.log(data[0][0]);
            da = JSON.parse(data[0][0]);

            console.log(da);
            // console.log(data[0].length);
            console.log(da[1] * 29.97 - 100);

            for (i = 1; i < Object.keys(da).length / 29.97; i++) {
                datas['labels'].push(i); //1個目のデータセットを追加
                datas['datasets'][1]['data'].push(da[Math.round(i * 29.97)] - 100);
                datass['labels'].push(i); //1個目のデータセットを追加
                datass['datasets'][1]['data'].push(da[Math.round(i * 29.97)] - 100);
            }


        }).fail(function (XMLHttpRequest, textStatus, errorThrown) {
            console.log('通信に失敗しました');
            console.log("XMLHttpRequest : " + XMLHttpRequest.status);
            console.log("textStatus     : " + textStatus);
            console.log("errorThrown    : " + errorThrown.message);
        });


    ext_chart = new Chart(ctxt, {
        type: 'line',
        data: datas,
        options: options
    });

    ext_chart = new Chart(ctxt, {
        type: 'line',
        data: datass,
        options: option
    });
}


