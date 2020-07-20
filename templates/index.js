
Date.prototype.Format = function (fmt) { //author: meizz 
    var o = {
        "M+": this.getMonth() + 1,                 //月份 
        "d+": this.getDate(),                    //日 
        "h+": this.getHours(),                   //小时 
        "m+": this.getMinutes(),                 //分 
        "s+": this.getSeconds(),                 //秒 
        "q+": Math.floor((this.getMonth() + 3) / 3), //季度 
        "S": this.getMilliseconds()             //毫秒 
    };
    if (/(y+)/.test(fmt))
        fmt = fmt.replace(RegExp.$1, (this.getFullYear() + "").substr(4 - RegExp.$1.length));
    for (var k in o)
        if (new RegExp("(" + k + ")").test(fmt))
            fmt = fmt.replace(RegExp.$1, (RegExp.$1.length == 1) ? (o[k]) : (("00" + o[k]).substr(("" + o[k]).length)));
    return fmt;
}

function submit() {
    var un = $("#text_username").val()
    var pd = $("#text_password").val()
    var data = { "username": un, "password": pd }
    $.post("/api/register", JSON.stringify(data), function (msg) {
        var obj = JSON.parse(msg)
        $("#p_message").html(obj['message'])
        html = ""
        for (i = 0; i < obj['data'].length; i++) {
            var date = new Date(parseInt(obj['data'][i]["checktime"]) * 1000)
            html += "<p> checktime= " + date.Format("yyyy-MM-dd hh:mm:ss") + " message = " + obj['data'][i]["message"] + "</p>"
        }
        $("#div_log").html(html)
    })
}