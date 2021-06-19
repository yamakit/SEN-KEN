window.onload = getPrefData();

function getPrefData() {
    $.ajax({
        type: "POST",
        url: "../PHP/login.php",
        dataType: "json",
        cache: false,
        success: function (PrefData) {
            console.log(PrefData);
            // select の内容削除
            $("#SelectPref").empty();
            var append = '<option value=""></option>&#10;';
            // JSON データを option に展開生成
            for (var i = 0; i < PrefData.length; i++) {
                append += '<option value="' + PrefData[i].id + '" >';
                append += PrefData[i].name;
                append += '</option>';
                append += '&#10;';
            }
            // select の内容に設定
            $("#SelectPref").append(append);
        }
    });
    return false;
}

