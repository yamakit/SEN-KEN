//プルダウンに変更があった時実行
function select() {
    const question = document.form1.pull;//要素を取得
    const num = question.selectedIndex;//選択されている要素の番号を格納する
    const str = question.options[num].value;//選択されたオプションの決められたvalueを格納する
    console.log(str);

    const url = 'conn.php?begin=' + str;
    let response = fetch(url)
        .then(response => response.json())
        .then(data => {
            console.log(data);
            // const button = [];
            // const button_rate = [];
            // for (let i = 1; i < 9; i++) {
            //     button.push(data[i]['correct_count'] + "/" + data[i]['question_count'])
            //     button_rate.push(data[i]['correct_rate']);
            // }
            // console.log(button[0])
            // if (data[0]['question_count'] == 0) {
            //     const button1 = 0 + "/" + 0;
            //     //const button1_rate = 100;
            // } else {
            //     const button1 = data[0]['correct_count'] + "/" + data[0]['question_count']
            //     const button1_rate = data[0]['correct_rate'];
            // }
            const button1 = data[0]['correct_count'] + "/" + data[0]['question_count']
            const button2 = data[1]['correct_count'] + "/" + data[1]['question_count']
            const button3 = data[2]['correct_count'] + "/" + data[2]['question_count']
            const button4 = data[3]['correct_count'] + "/" + data[3]['question_count']
            const button5 = data[4]['correct_count'] + "/" + data[4]['question_count']
            const button6 = data[5]['correct_count'] + "/" + data[5]['question_count']
            const button7 = data[6]['correct_count'] + "/" + data[6]['question_count']
            const button8 = data[7]['correct_count'] + "/" + data[7]['question_count']
            const button9 = data[8]['correct_count'] + "/" + data[8]['question_count']


            const button1_rate = data[0]['correct_rate'];
            const button2_rate = data[1]['correct_rate'];
            const button3_rate = data[2]['correct_rate'];
            const button4_rate = data[3]['correct_rate'];
            const button5_rate = data[4]['correct_rate'];
            const button6_rate = data[5]['correct_rate'];
            const button7_rate = data[6]['correct_rate'];
            const button8_rate = data[7]['correct_rate'];
            const button9_rate = data[8]['correct_rate'];

            const total = (button1_rate + button2_rate + button3_rate + button4_rate + button5_rate + button6_rate + button7_rate + button8_rate + button9_rate) / 9
            console.log(total);

            //home.htmlの<table>ないのデータを書き換え
            document.getElementById("td1").innerHTML = button1 + "\n" + button1_rate + '%';
            document.getElementById("td2").innerHTML = button2 + '\n' + button2_rate + '%';
            document.getElementById("td3").innerHTML = button3 + '\n' + button3_rate + '%';
            document.getElementById("td4").innerHTML = button4 + '\n' + button4_rate + '%';
            document.getElementById("td5").innerHTML = button5 + '\n' + button5_rate + '%';
            document.getElementById("td6").innerHTML = button6 + '\n' + button6_rate + '%';
            document.getElementById("td7").innerHTML = button7 + '\n' + button7_rate + '%';
            document.getElementById("td8").innerHTML = button8 + '\n' + button8_rate + '%';
            document.getElementById("td9").innerHTML = button9 + '\n' + button9_rate + '%';
            return total;
        });

}

function chart() {
    console.log(total);
}

