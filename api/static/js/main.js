// setTimeout("dengchang()",6666)
//#触发登场：倒计时或者滑到底部
dengchangCnt=0;
setTimeout("dengchang()",6666)

function dengchang() {
    if(dengchangCnt>0){
        return
    }
    dengchangCnt+=1
    $("#company")[0].style.display = "block";
    zoomup("company");
    window.onscroll = function () { }

}
window.onscroll = function () {
    if (getScrollTop() + getWindowHeight() >= getScrollHeight() - 10) {
        dengchang();
          //移除该事件
        // 这里可以调用接口请求数据了，滑动到底部自动加载数据
    }
};


//滚动条在Y轴上的滚动距离

function getScrollTop() {
    var scrollTop = 0, bodyScrollTop = 0, documentScrollTop = 0;
    if (document.body) {
        bodyScrollTop = document.body.scrollTop;
    }
    if (document.documentElement) {
        documentScrollTop = document.documentElement.scrollTop;
    }
    scrollTop = (bodyScrollTop - documentScrollTop > 0) ? bodyScrollTop : documentScrollTop;
    return scrollTop;
}



//文档的总高度

function getScrollHeight() {
    var scrollHeight = 0, bodyScrollHeight = 0, documentScrollHeight = 0;
    if (document.body) {
        bodyScrollHeight = document.body.scrollHeight;
    }
    if (document.documentElement) {
        documentScrollHeight = document.documentElement.scrollHeight;
    }
    scrollHeight = (bodyScrollHeight - documentScrollHeight > 0) ? bodyScrollHeight : documentScrollHeight;
    return scrollHeight;
}



//浏览器视口的高度

function getWindowHeight() {
    var windowHeight = 0;
    if (document.compatMode == "CSS1Compat") {
        windowHeight = document.documentElement.clientHeight;
    } else {
        windowHeight = document.body.clientHeight;
    }
    return windowHeight;
}





var mode = null

$('#aes').click(function () {
    $('#des')[0].checked = false;
    if ($('#des')[0].checked == false && $('#aes')[0].checked == false) {
        mode = null;

    }
    else mode = 'AES';
    EncryptTest();
    DecryptTest();
    // alert(mode)
})

$('#des').click(function () {
    $('#aes')[0].checked = false;
    if ($('#des')[0].checked == false && $('#aes')[0].checked == false) {
        mode = null;
    }
    else mode = 'DES';
    EncryptTest();
    DecryptTest();
})

function EncryptTest() {
    // console.log($('#input_text').val())
    if ($('#input_text').val() === "" || mode === null) {
        $("#Encrypt").attr("disabled", "true")
        return
    }

    else $("#Encrypt").removeAttr("disabled");
}

function DecryptTest() {
    if ($('#output_text').val() === "" || mode === null) {
        $("#Decrypt").attr("disabled", "true")
        return
    }
    else $("#Decrypt").removeAttr("disabled");
}

//onchange不够智能，要将焦点移出时才会触发，这里是相当于计算剩余字数，只要有变化就会触发
$('#input_text').bind('input propertychange', 'textarea', function () {
    EncryptTest();
})

$('#output_text').bind('input propertychange', 'textarea', function () {
    DecryptTest();
})

// $('#input_text').change(function (){
//
//
//
// })


// $('#DES').click(function(){
//     mode = 'DES'
// })
//
// $('#AES').click(function(){
//     mode = 'AES'
// })


function zoomOut(id) {
    const element = document.getElementById(id);
    const className = "animate__zoomOut"
    element.classList.add(className);
    element.style.setProperty('--animate-duration', '0.25s');
    element.addEventListener('animationend', () => {
        element.classList.remove(className);
    });
}

function zoomIn(id) {
    const element = document.getElementById(id);
    const className = "animate__zoomIn"
    element.classList.add(className);
    element.style.setProperty('--animate-duration', '0.7s');
    element.addEventListener('animationend', () => {
        element.classList.remove(className);
    });
}

function shake(id) {
    const element = document.getElementById(id);
    const className = "animate__headShake"
    element.classList.add(className);
    element.style.setProperty('--animate-duration', '0.7s');
    element.addEventListener('animationend', () => {
        element.classList.remove(className);
    });
}

function backUp(id) {
    const element = document.getElementById(id);
    const className = "animate__backInUp"
    element.classList.add(className);
    element.style.setProperty('--animate-duration', '0.3s');
    element.addEventListener('animationend', () => {
        element.classList.remove(className);
    });
}

function zoomup(id) {
    const element = document.getElementById(id);
    const className = "animate__zoomInUp"
    element.classList.add(className);
    element.style.setProperty('--animate-duration', '1.6s');
    element.addEventListener('animationend', () => {
        element.classList.remove(className);
    });
}



$('#Encrypt').click(function () {
    var key = $('#keyInput').val()
    var expt = $('#input_text').val()

    // console.log(expt)
    data_ = { 'key': key, 'expt': expt, 'mode': mode }
    console.log(data_)

    $.ajax({
        url: '/Encrypt',
        type: "POST",
        dataType: "json",
        data: data_,
        success: function (data) {
            alertHide();
            zoomOut("input_text")
            console.log(data)
            $('#output_text').val(data['str_cipt'])
            zoomIn("output_text")
            DecryptTest();

        }
    })

})

$('#Decrypt').click(function () {
    var key = $('#keyInput').val()
    var cipt = $('#output_text').val()
    // console.log(key)
    data_ = { 'key': key, 'cipt': cipt, 'mode': mode }
    $.ajax({
        url: '/Decrypt',
        type: "POST",
        dataType: "json",
        data: data_,
        success: function (data) {
            alertHide();
            zoomOut("output_text")
            console.log(data)
            $('#input_text').val(data['str_expt'])
            zoomIn("input_text")
            EncryptTest();
        },
        error: function () {
            raiseDecryptionError();
            alertShow();
        }
    })

})


function raiseDecryptionError() {

    shake("output_text");
    alertShow();
}


$("#encryptClear").click(function () {
    document.getElementById("input_text").value = "";
    EncryptTest();
})
$("#decryptClear").click(function () {
    document.getElementById("output_text").value = "";
    DecryptTest();
})


$('#uploadKey').click(function () {
    $('#euploadkey').click()
})


$('#euploadtxt').click(function () {
    $('#eupload').click()
})


$('#cuploadtxt').click(function () {
    $('#cupload').click()
})

var openFile1 = function (event) {

    var input = event.target;
    // console.log(input.value)
    var sourceId = event.target.id;
    var textElement = null;
    // console.log(input)
    var reader = new FileReader();
    reader.onload = function () {
        if (reader.result) {
            //显示文件内容
            if (sourceId == "euploadkey") {
                textElement = $("#keyInput")[0]
            }
            if (sourceId == "eupload") {
                textElement = $("#input_text")[0]
                setTimeout("EncryptTest();", 100);
            }

            textElement.value = reader.result;
        }
    };
    reader.readAsText(input.files[0]);
    input.value = "";  //优化，设置value值为空，这样的话防止为空

};

var openFile2 = function (event) {
    var input = event.target;
    var reader = new FileReader();
    reader.onload = function () {
        if (reader.result) {
            //显示文件内容
            $("#output_text").text(reader.result);
            setTimeout("DecryptTest();", 100);
        }
    };
    reader.readAsText(input.files[0]);

};

function download1() {
    var text = $("#input_text").val()
    console.log(text)
    var blob = new Blob([text], { type: "text/plain" });
    var anchor = document.createElement("a");
    //anchor.download = "my-filename.txt"; 
    anchor.download = 'Plain_text';
    anchor.href = window.URL.createObjectURL(blob);
    anchor.target = "_blank";
    anchor.style.display = "none"; // just to be safe! 
    document.body.appendChild(anchor);
    anchor.click();
    document.body.removeChild(anchor);
}

function download2() {
    var text = $("#output_text").val()
    var blob = new Blob([text], { type: "text/plain" });
    var anchor = document.createElement("a");
    //anchor.download = "my-filename.txt"; 
    anchor.download = 'Cipher_text';
    anchor.href = window.URL.createObjectURL(blob);
    anchor.target = "_blank";
    anchor.style.display = "none"; // just to be safe! 
    document.body.appendChild(anchor);
    anchor.click();
    document.body.removeChild(anchor);
}


function alertHide() {
    $("#decryptAlert").hide();
}

function alertShow() {
    $("#decryptAlert").show();
    backUp("decryptAlert");
}