
var more;
let most;
var randoms = [];
var randnumarray = [0, 0, 0, 0];

window.onload = function () {　//リンクからプレイヤーidとボールidを取得
    var data = location.href.split("?")[1];
    console.log(data);
    var text = data.split("=")[1];
    console.log(text);
    more = text.split("&")[0];
    console.log("プレイヤーid :", more);
    most = text.split("&")[1];
    console.log("ボールid :", most);
    // if (most == "submit") {
    // }
    sent();
}

function receive() {　//予想クイズへ遷移
    location.href = "../HTML/index.html?data=" + more + "&" + most;
}

function attack() {　//打ち方分析へ遷移
    location.href = "../HTML/attack.html?data=" + more + "&" + most;
}
var name;
var affiliation;
var position;
var u;
function sent() {　//データベースからユーザーの情報を取得
    console.log("sent()が呼び出されました！！");
    $.ajax({
        type: "GET",
        url: "../PHP/home.php",
        dataType: "json",
        data: {
            'player_id': more,
            'ball_id': most,
        },
    })
        .done(function (data) {
            console.log('DONE', data);
            console.log("通信が成功しました!!!");
            most = data[0][0][1];
            detailobject = document.getElementById("detail");
            link = ' <a class="myself"></br>名前：' + data[0][0][2] + '</br > 所属：' + data[0][0][3] + '</br > 一言：' + data[0][0][4] + '</a >';
            face.setAttribute("src", data[0][0][5]);
            detailobject.insertAdjacentHTML('beforeend', link);
            console.log("ボールid :", most);
            datas['datasets'][0]['label'] = data[0][0][2];
            datas['datasets'][1]['label'] = data[1][0][2];
            datas['datasets'][2]['label'] = data[1][1][2];
            datas['datasets'][3]['label'] = data[1][2][2];
            datas['datasets'][4]['label'] = data[1][3][2];
            randnumarray = [data[1][0][0], data[1][1][0], data[1][2][0], data[1][3][0]]
            console.log(randnumarray);
            graph();

        }).fail(function (XMLHttpRequest, textStatus, errorThrown) {
            console.log('通信に失敗しました');
            console.log("XMLHttpRequest : " + XMLHttpRequest.status);
            console.log("textStatus     : " + textStatus);
            console.log("errorThrown    : " + errorThrown.message);
        });

}

// var count = 0;
// function select() {
//     const question = document.form1.pull;//要素を取得
//     const num = question.selectedIndex;//選択されている要素の番号を格納する
//     const str = question.options[num].value;//選択されたオプションの決められたvalueを格納する
//     console.log(str);

//     const url = '../PHP/conn.php?begin=' + str;
//     let response = fetch(url)
//         .then(response => response.json())
//         .then(data => {
//             console.log(data);

//             const button1 = data[0]['correct_count'] + "/" + data[0]['question_count']
//             const button2 = data[1]['correct_count'] + "/" + data[1]['question_count']
//             const button3 = data[2]['correct_count'] + "/" + data[2]['question_count']
//             const button4 = data[3]['correct_count'] + "/" + data[3]['question_count']
//             const button5 = data[4]['correct_count'] + "/" + data[4]['question_count']
//             const button6 = data[5]['correct_count'] + "/" + data[5]['question_count']
//             const button7 = data[6]['correct_count'] + "/" + data[6]['question_count']
//             const button8 = data[7]['correct_count'] + "/" + data[7]['question_count']
//             const button9 = data[8]['correct_count'] + "/" + data[8]['question_count']


//             const button1_rate = data[0]['correct_rate'];
//             const button2_rate = data[1]['correct_rate'];
//             const button3_rate = data[2]['correct_rate'];
//             const button4_rate = data[3]['correct_rate'];
//             const button5_rate = data[4]['correct_rate'];
//             const button6_rate = data[5]['correct_rate'];
//             const button7_rate = data[6]['correct_rate'];
//             const button8_rate = data[7]['correct_rate'];
//             const button9_rate = data[8]['correct_rate'];

//             const total = (button1_rate + button2_rate + button3_rate + button4_rate + button5_rate + button6_rate + button7_rate + button8_rate + button9_rate) / 9
//             console.log(total);

//             //home.htmlの<table>ないのデータを書き換え
//             document.getElementById("td1").innerHTML = button1 + "\n" + button1_rate + '%';
//             document.getElementById("td2").innerHTML = button2 + '\n' + button2_rate + '%';
//             document.getElementById("td3").innerHTML = button3 + '\n' + button3_rate + '%';
//             document.getElementById("td4").innerHTML = button4 + '\n' + button4_rate + '%';
//             document.getElementById("td5").innerHTML = button5 + '\n' + button5_rate + '%';
//             document.getElementById("td6").innerHTML = button6 + '\n' + button6_rate + '%';
//             document.getElementById("td7").innerHTML = button7 + '\n' + button7_rate + '%';
//             document.getElementById("td8").innerHTML = button8 + '\n' + button8_rate + '%';
//             document.getElementById("td9").innerHTML = button9 + '\n' + button9_rate + '%';
//             return total;
//         });

// }

// function chart() {
//     const question = document.form2.pull;//要素を取得
//     const num = question.selectedIndex;//選択されている要素の番号を格納する
//     const str = question.options[num].value;//選択されたオプションの決められたvalueを格納する
//     console.log(str);
//     assumed = str;
//     send();
//     const url = '../PHP/chart.php?begin=' + str;
//     let response = fetch(url)
//         .then(response => response.json())
//         .then(data => {
//             console.log(data);
//             labels = []; //ajaxのたびに初期化するので[]を代入する
//             datasets = [];

//             datasets['y'] = {
//                 label: 'aaa',
//                 data: [],
//                 backgroundColor: [
//                     'rgba(255, 99, 132, 0.2)',
//                     'rgba(54, 162, 235, 0.2)',
//                     'rgba(255, 206, 86, 0.2)',
//                     'rgba(75, 192, 192, 0.2)',
//                     'rgba(153, 102, 255, 0.2)',
//                     'rgba(255, 159, 64, 0.2)'
//                 ],
//                 borderColor: [
//                     'rgba(255, 99, 132, 1)',
//                     'rgba(54, 162, 235, 1)',
//                     'rgba(255, 206, 86, 1)',
//                     'rgba(75, 192, 192, 1)',
//                     'rgba(153, 102, 255, 1)',
//                     'rgba(255, 159, 64, 1)'
//                 ],
//                 borderWidth: 1,
//                 lineTension: 0,
//                 fill: false,
//                 borderWidth: 3

//             };


//             var x = 0;
//             $.each(data, function (index) {
//                 if (data[index].judge == 1) {

//                     x = count++;
//                     console.log(x);
//                     // labels.push(index);
//                     // datasets['y']['data'].push(x); //1個目のデータセットを追加
//                 }
//                 labels.push(index + 1);
//                 datasets['y']['data'].push(x); //1個目のデータセットを追加
//             });

//             var ctx = document.getElementById('myChart').getContext('2d');
//             var myChart = new Chart(ctx, {
//                 type: 'line',
//                 data: {
//                     labels: labels,//各棒の名前（name)
//                     // labels: ['Red', 'Blue', 'Yellow', 'Green', 'Purple', 'ほげ'],//各棒の名前（name)
//                     datasets: [datasets['y']]
//                 },
//                 options: {
//                     scales: {
//                         yAxes: [{
//                             ticks: {
//                                 beginAtZero: true,
//                                 userCallback: function (label, index, labels) {
//                                     if (Math.floor(label) === label) {
//                                         return label;
//                                     }
//                                 }
//                             }
//                         }]
//                     }
//                 }
//             });
//         });



var assumed = 0;
// }
const ctx = document.getElementById('myChart');
var datas = {
    labels: [],
    datasets: [{
        label: '',
        data: [],
        borderColor: 'red',
        // pointBackgroundColor: 'rgba(255, 100, 100, 1)',
        pointRadius: 7,
        lineTension: 0,
        fill: false,
        borderWidth: 3
    },
    {
        label: '',
        data: [],
        borderColor: 'blue',
        // pointBackgroundColor: 'rgba(255, 100, 100, 1)',
        pointRadius: 7,
        lineTension: 0,
        fill: false,
        borderWidth: 3
    },
    {
        label: '',
        data: [],
        borderColor: 'yellow',
        // pointBackgroundColor: 'rgba(255, 100, 100, 1)',
        pointRadius: 7,
        lineTension: 0,
        fill: false,
        borderWidth: 3
    },
    {
        label: '',
        data: [],
        borderColor: 'green',
        // pointBackgroundColor: 'rgba(255, 100, 100, 1)',
        pointRadius: 7,
        lineTension: 0,
        fill: false,
        borderWidth: 3
    },
    {
        label: '',
        data: [],
        borderColor: 'purple',
        // pointBackgroundColor: 'rgba(255, 100, 100, 1)',
        pointRadius: 7,
        lineTension: 0,
        fill: false,
        borderWidth: 3
    },
    ],
}

var option = {
    animation: false,
    events: [],
    scales: {
        xAxes: [{
            scaleLabel: {
                display: true,
                labelString: '日数'
            }
        }],
        yAxes: [{
            ticks: {
                min: 0,
                max: 100,
                stepSize: 10,
                userCallback: function (tick) {
                    return tick.toString() + '%';
                }
            },
            scaleLabel: {
                display: true,
                labelString: '正答率'
            }
        }]
    },
    title: {
        display: true,
        text: '3日の正解率と日にちの関係'
    }
};
var ex_chart = new Chart(ctx, {
    type: 'line',
    data: datas,
    options: option
});

var sumarray = [];
var dataarray = [0, 0, 0, 0, 0];
var shift = 0;
function graph() {   //データベースから直近◯日分のデータの数を取得
    console.log("graph()が呼び出されました！！");
    const question = document.form2.pull;//要素を取得
    const num = question.selectedIndex;//選択されている要素の番号を格納する
    const str = question.options[num].value;//選択されたオプションの決められたvalueを格納する
    console.log(str);
    assumed = str;
    console.log(assumed);
    sum = 0;
    option.title.text = assumed + '日の正解率と日にちの関係';

    // for (i = 0; i < shift; i++) {
    //     datas['datasets'][0]['data'].pop();
    //     datas['datasets'][1]['data'].pop();
    //     datas['datasets'][2]['data'].pop();
    //     datas['datasets'][3]['data'].pop();
    //     datas['datasets'][4]['data'].pop();
    //     datas['labels'].shift();
    // }
    datas['datasets'][0]['data'].length = 0;
    datas['datasets'][1]['data'].length = 0;
    datas['datasets'][2]['data'].length = 0;
    datas['datasets'][3]['data'].length = 0;
    datas['datasets'][4]['data'].length = 0;
    datas['labels'].length = 0;


    $.ajax({
        type: "GET",
        url: "../PHP/home2.php",
        dataType: "json",
        data: {
            'player_id': more,
            'randnum0': randnumarray[0],
            'randnum1': randnumarray[1],
            'randnum2': randnumarray[2],
            'randnum3': randnumarray[3],
            'day': str,
        },
    })
        .done(function (data) {
            console.log('DONE', data);
            console.log("通信が成功しました!!!");

            sumarray = [0, 0, 0, 0, 0];
            console.log(data[0].length);
            for (i = 0; i < data.length; i++) {
                for (j = 0; j < data[i].length; j++) {
                    sumarray[i] = sumarray[i] + Number(data[i][j]);
                }
                dataarray[i] = data[i];
            }
            console.log(dataarray);
            console.log(sumarray);
            for (i = 0; i < data[0].length; i++) {
                sum = sum + Number(data[i]);
            }
            // k = data;
            // console.log("sum :", sum);

            // for (i = 0; i < data.length; i++) {
            //     sum2 = sum2 + Number(data[i]);
            // }
            // l = data;
            // console.log("sum2", sum2);

            // for (i = 0; i < data.length; i++) {
            //     sum3 = sum3 + Number(data[i]);
            // }
            // m = data;
            // console.log("sum3", sum3);


            // for (i = 0; i < data.length; i++) {
            //     sum4 = sum4 + Number(data[i]);
            // }
            // n = data;
            // console.log("sum4", sum4);


            // for (i = 0; i < data.length; i++) {
            //     sum5 = sum5 + Number(data[i]);
            // }
            // o = data;
            // console.log("sum5", sum5);
            var p = 0;
            for (i = 0; i < sumarray.length; i++) {
                p = p + sumarray[i];
            }
            console.log(p);
            if (p == 0) {
                nan.innerHTML = "※表示できるデータがありません。";
            }

        }).fail(function (XMLHttpRequest, textStatus, errorThrown) {
            console.log('通信に失敗しました');
            console.log("XMLHttpRequest : " + XMLHttpRequest.status);
            console.log("textStatus     : " + textStatus);
            console.log("errorThrown    : " + errorThrown.message);
        });




    a = Number(str) + 1;
    for (i = 1; i < a; i++) {
        datas['labels'].push(i + '日目');
    }

    setTimeout(send, 100);
};



function send() {　　　 //データベースから直近◯日分のデータの数だけデータを取得、グラフを描画、表に数字を表示
    console.log("send()が呼び出されました！！");
    $.ajax({
        type: "GET",
        url: "../PHP/home3.php",
        dataType: "json",
        data: {
            'player_id': more,
            'randnum0': randnumarray[0],
            'randnum1': randnumarray[1],
            'randnum2': randnumarray[2],
            'randnum3': randnumarray[3],
            'sum': sumarray[0],
            'sum2': sumarray[1],
            'sum3': sumarray[2],
            'sum4': sumarray[3],
            'sum5': sumarray[4],

        },
    })
        .done(function (data) {
            console.log('DONE', data);
            console.log("通信が成功しました!!!");

            button1 = [];
            button1judge = [];
            button2 = [];
            button2judge = [];
            button3 = [];
            button3judge = [];
            button4 = [];
            button4judge = [];
            button5 = [];
            button5judge = [];
            button6 = [];
            button6judge = [];
            button7 = [];
            button7judge = [];
            button8 = [];
            button8judge = [];
            button9 = [];
            button9judge = [];



            for (i = 0; i < data[0].length; i++) {
                if (data[0][i]['button_id'] == 1) {
                    button1.push(data[0][i]['judge']);
                } else if (data[0][i]['button_id'] == 2) {
                    button2.push(data[0][i]['judge']);
                } else if (data[0][i]['button_id'] == 3) {
                    button3.push(data[0][i]['judge']);
                } else if (data[0][i]['button_id'] == 4) {
                    button4.push(data[0][i]['judge']);
                } else if (data[0][i]['button_id'] == 5) {
                    button5.push(data[0][i]['judge']);
                } else if (data[0][i]['button_id'] == 6) {
                    button6.push(data[0][i]['judge']);
                } else if (data[0][i]['button_id'] == 7) {
                    button7.push(data[0][i]['judge']);
                } else if (data[0][i]['button_id'] == 8) {
                    button8.push(data[0][i]['judge']);
                } else if (data[0][i]['button_id'] == 9) {
                    button9.push(data[0][i]['judge']);
                }
            }
            for (i = 0; i < button1.length; i++) {
                if (button1[i] == 1) {
                    button1judge.push(button1[i]);
                }
            }
            for (i = 0; i < button2.length; i++) {
                if (button2[i] == 1) {
                    button2judge.push(button2[i]);
                }
            }
            for (i = 0; i < button3.length; i++) {
                if (button3[i] == 1) {
                    button3judge.push(button3[i]);
                }
            }
            for (i = 0; i < button4.length; i++) {
                if (button4[i] == 1) {
                    button4judge.push(button4[i]);
                }
            }
            for (i = 0; i < button5.length; i++) {
                if (button5[i] == 1) {
                    button5judge.push(button5[i]);
                }
            }
            for (i = 0; i < button6.length; i++) {
                if (button6[i] == 1) {
                    button6judge.push(button6[i]);
                }
            }
            for (i = 0; i < button7.length; i++) {
                if (button7[i] == 1) {
                    button7judge.push(button7[i]);
                }
            }
            for (i = 0; i < button8.length; i++) {
                if (button8[i] == 1) {
                    button8judge.push(button8[i]);
                }
            }
            for (i = 0; i < button9.length; i++) {
                if (button9[i] == 1) {
                    button9judge.push(button9[i]);
                }
            }

            if (button1.length == 0) { percentage1 = 0 } else { percentage1 = Math.round(button1judge.length / button1.length * 100); }
            if (button2.length == 0) { percentage2 = 0 } else { percentage2 = Math.round(button2judge.length / button2.length * 100); }
            if (button3.length == 0) { percentage3 = 0 } else { percentage3 = Math.round(button3judge.length / button3.length * 100); }
            if (button4.length == 0) { percentage4 = 0 } else { percentage4 = Math.round(button4judge.length / button4.length * 100); }
            if (button5.length == 0) { percentage5 = 0 } else { percentage5 = Math.round(button5judge.length / button5.length * 100); }
            if (button6.length == 0) { percentage6 = 0 } else { percentage6 = Math.round(button6judge.length / button6.length * 100); }
            if (button7.length == 0) { percentage7 = 0 } else { percentage7 = Math.round(button7judge.length / button7.length * 100); }
            if (button8.length == 0) { percentage8 = 0 } else { percentage8 = Math.round(button8judge.length / button8.length * 100); }
            if (button9.length == 0) { percentage9 = 0 } else { percentage9 = Math.round(button9judge.length / button9.length * 100); }


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
            // var buttonjudgeArray = [button1judge, button2judge, button3judge, button4judge, button5judge, button6judge, button7judge, button8judge, button9judge];
            var buttonArray = [button1, button2, button3, button4, button5, button6, button7, button8, button9];
            var percentageArray = [percentage1, percentage2, percentage3, percentage4, percentage5, percentage6, percentage7, percentage8, percentage9];

            color1.innerHTML = button1judge.length + "/" + button1.length + "\n" + percentage1 + "%";
            color2.innerHTML = button2judge.length + "/" + button2.length + "\n" + percentage2 + "%";
            color3.innerHTML = button3judge.length + "/" + button3.length + "\n" + percentage3 + "%";
            color4.innerHTML = button4judge.length + "/" + button4.length + "\n" + percentage4 + "%";
            color5.innerHTML = button5judge.length + "/" + button5.length + "\n" + percentage5 + "%";
            color6.innerHTML = button6judge.length + "/" + button6.length + "\n" + percentage6 + "%";
            color7.innerHTML = button7judge.length + "/" + button7.length + "\n" + percentage7 + "%";
            color8.innerHTML = button8judge.length + "/" + button8.length + "\n" + percentage8 + "%";
            color9.innerHTML = button9judge.length + "/" + button9.length + "\n" + percentage9 + "%";

            c0 = '#FFFFFF80';
            c1 = '#ff000080';
            c2 = '#ffa50080';
            c3 = '#ffff0080';
            c4 = '#00FF0080';
            c5 = '#0033FF80';

            var colorArray = [c1, c2, c3, c4, c5];

            for (let item in buttonArray) {
                // if (buttonArray[item].length == 0) {
                //     tdArray[item].style.backgroundColor = c0;
                // } else
                if (percentageArray[item] == 100) {
                    tdArray[item].style.backgroundColor = colorArray[4];
                } else {

                    let n = parseInt(percentageArray[item] / parseInt((100 / (colorArray.length))));
                    tdArray[item].style.backgroundColor = colorArray[n];
                }

            }

            console.log(data[0]);
            for (f = 0; f < data.length; f++) {
                console.log(f + 1, "人目");

                for (p = 0; p < assumed; p++) {
                    arr = 0;
                    for (i = 0; i < dataarray[f][p]; i++) {
                        if (data[f][i]['judge'] == 1) {
                            arr = arr + 1;
                        }
                    }
                    var one = arr / dataarray[f][p] * 100;
                    datas['datasets'][f]['data'].push(one);
                    console.log(one);
                    console.log(datas['datasets'][f]['data']);
                }
            }
            // for (p = 0; p < assumed; p++) {
            //     arr = 0;
            //     for (i = 0; i < dataarray[1][p]; i++) {
            //         if (data[i]['judge'] == 1) {
            //             arr = arr + 1;
            //         }
            //     }
            //     var two = arr / dataarray[1][p] * 100;
            //     datas['datasets'][1]['data'].push(two);
            //     console.log(two);
            //     console.log(datas['datasets'][1]['data']);
            // }
            // for (p = 0; p < assumed; p++) {
            //     arr = 0;
            //     for (i = 0; i < dataarray[2][p]; i++) {
            //         if (data[i]['judge'] == 1) {
            //             arr = arr + 1;
            //         }
            //     }
            //     var three = arr / dataarray[2][p] * 100;
            //     datas['datasets'][2]['data'].push(three);
            //     console.log(three);
            //     console.log(datas['datasets'][2]['data']);
            // }
            // for (p = 0; p < assumed; p++) {
            //     arr = 0;
            //     for (i = 0; i < dataarray[3][p]; i++) {
            //         if (data[i]['judge'] == 1) {
            //             arr = arr + 1;
            //         }
            //     }
            //     var four = arr / dataarray[3][p] * 100;
            //     datas['datasets'][2]['data'].push(four);
            //     console.log(four);
            //     console.log(datas['datasets'][3]['data']);
            // }

            // for (p = 0; p < assumed; p++) {
            //     arr = 0;
            //     for (i = 0; i < dataarray[4][p]; i++) {
            //         if (data[i]['judge'] == 1) {
            //             arr = arr + 1;
            //         }
            //     }
            //     var five = arr / dataarray[4][p] * 100;
            //     datas['datasets'][4]['data'].push(five);
            //     console.log(five);
            //     console.log(datas['datasets'][4]['data']);
            // }


            shift = assumed;
            // console.log(datas);
            ex_chart = new Chart(ctx, {
                type: 'line',
                data: datas,
                options: option
            });
        }).fail(function (XMLHttpRequest, textStatus, errorThrown) {
            console.log('通信に失敗しました');
            console.log("XMLHttpRequest : " + XMLHttpRequest.status);
            console.log("textStatus     : " + textStatus);
            console.log("errorThrown    : " + errorThrown.message);
        });



}