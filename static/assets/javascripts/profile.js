//upload header image
$("#uploadHeadImg").on('change', function(){
    var file = document.querySelector("#uploadHeadImg").files[0];
    var min_width = 150;
    var min_height = 150;
    if (file && /\.(jpe?g|png|gif)$/i.test(file.name) ) {
         //读取图片数据
        var reader = new FileReader();
        reader.readAsDataURL(file);
        reader.onload = function (e) {
        var data = e.target.result;
            //加载图片获取图片真实宽度和高度
            var image = new Image();
            image.onload=function(){
                var width = this.width;
                var height = this.height;
                ifPreview(width, min_width, height, min_height, data, file, "headImg","head");
            };
            image.src= data;
        };
    }
    else{
        alert('格式不正确');
    }
});

$("#update-password").on('click', function () {
    var password = $("#password").val();
    var repassword = $("#password-confirmation").val();
    var pwdpattern = /^(?![0-9]+$)(?![a-zA-Z]+$)[0-9A-Za-z]{6,21}$/;
    var step = 1;
    if (step == 1) {
        if (password == "" || password == null) {
            danger("errorTips", "密码不能为空");
        }
        else {
            step = 2;
        }
    }
    if (step == 2) {
        if (pwdpattern.test(password) == false) {
            danger("errorTips", "密码由6-21字母和数字组成，不能是纯数字或纯英文");
        }
        else {
            step = 3;
        }
    }
    if (step == 3) {
        if (password != repassword) {
            danger("errorTips", "两次密码不匹配");
        }
        else {
            step = 4;
        }
    }
    if (step == 4) {
        $.ajax({
            type: "POST",
            url: "/profile/",
            data: { 'password': repassword, 'action':'resetpassword' },
            headers: {
                'X-CSRFToken': $.cookie('csrftoken')
            },
            async: true,
            error: function (request) {
                danger("errorTips", "对不起, 修改密码失败, 请稍后再试");
            },
            success: function (callback) {
                if(callback == 'success'){
                    window.location.href = '/profile/';
                }else{
                    danger("errorTips", '对不起, 修改密码失败, 请稍后再试');
                }
            }
        });
    }
});

$('#profile-save').on('click', function() {
    let nickname = $('#nickname').val();
    let teacherId = $('#select-teacher').val();
    let gradeId = Number($('#select-grade').val());
    let classId = Number($('#select-class').val());
    $.ajax({
        type: "POST",
        url: "/profile/",
        data: { 'nickname': nickname,
            'teacherId': teacherId,
            'gradeId': gradeId,
            'classId': classId,
            'action':'editprofile' },
        headers: {
            'X-CSRFToken': $.cookie('csrftoken')
        },
        async: true,
        error: function (request) {
            danger("errorTips", "对不起, 编辑失败, 请稍后再试");
        },
        success: function (callback) {
            if(callback == 'success'){
                window.location.href = '/profile/';
            }else{
                danger("errorTips", '对不起, 编辑失败, 请稍后再试');
            }
        }
    });
});

function danger(tid, tips) {
    $("#" + tid).removeClass('hidden').text(tips);
}
function removeTips(tid) {
    $("#" + tid).addClass("hidden");
}

function ifPreview(width, min_width, height, min_height, data, file, id, prefix){
    if(width < min_width || height < min_height){
        alert("请上传宽度大于 "+min_width+"px，高度大于 "+min_height+"px 的封面图片。");
    }
    else{
        //preview and update
        $("#"+id).attr("src", data);
        imgUpload(file, prefix);
    }
}

function imgUpload(file, prefix) {
    var formData = new FormData();
    formData.append("imgFile", file);
    formData.append("prefix", prefix);
    ajax(formData, "/upload_imgs/");
}

function ajax(formData, URL){
    $.ajax({
        type:'POST',
        url: URL,
        data: formData,
        headers: {
            'X-CSRFToken': $.cookie('csrftoken')
        },
        processData: false,
        contentType: false,
        async: false,
        success: function(callback) {
            window.location.reload();
        }
    });
}

//proile update
