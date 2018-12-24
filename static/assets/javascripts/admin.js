//display the error messeges
function danger(tid, tips) {
    $("#" + tid).removeClass('hidden').find('strong').text(tips);
}
(function () {
    $(document).ready = function () { };
    $('#gradeEdit').on('click', function () {
        var gradeId = $('#gradeId').val();
        var gradeName = $('#gradeName').val();
        var gradeDes = $('#gradeDes').val();
        var volume = $('#volume').val();
        var data = {
            'gradeId': gradeId,
            'gradeName': gradeName,
            'gradeDes': gradeDes,
            'volume': volume,
        }
        if (gradeName == '' || gradeName == undefined) {
            $('#errorTips').removeClass('hidden').find('strong').text('年级名不能为空');
        }
        else {
            $.ajax({
                type: 'POST',
                url: '/gradeManage/',
                data: data,
                headers: {
                    'X-CSRFToken': $.cookie('csrftoken')
                },
                async: false,
                err: function () {

                },
                success: function (callback) {
                    if (callback == 'success') {
                        window.location.href = "/grades/";
                    } else {
                        $('#errorTips').removeClass('hidden').find('strong').text(callback);
                    }
                }
            });
        }
    });
    $('#classEdit').on('click', function () {
        var gradeId = $('#gradeId').val();
        var classId = $('#classId').val();
        var className = $('#className').val();
        var classDes = $('#classDes').val();
        var data = {
            'gradeId': gradeId,
            'classId': classId,
            'className': className,
            'classDes': classDes
        }
        if (gradeId == '0' || gradeId == '' || gradeId == undefined) {
            $('#errorTips').removeClass('hidden').find('strong').text('请选择年级');
        }
        else if (className == '' || className == undefined) {
            $('#errorTips').removeClass('hidden').find('strong').text('班级名不能为空');
        }
        else {
            $.ajax({
                type: 'POST',
                url: '/classManage/',
                data: data,
                headers: {
                    'X-CSRFToken': $.cookie('csrftoken')
                },
                async: false,
                err: function () {

                },
                success: function (callback) {
                    if (callback == 'success') {
                        window.location.href = "/classes/";
                    } else {
                        $('#errorTips').removeClass('hidden').find('strong').text(callback);
                    }
                }
            });
        }
    });
    $('#courseEdit').on('click', function () {
        var gradeId = $('#gradeId').val();
        var volume = $('#volume').val();
        var courseId = $('#courseId').val();
        var courseName = $('#courseName').val();
        var courseDes = $('#courseDes').val();
        var data = {
            'gradeId': gradeId,
            'courseId': courseId,
            'courseName': courseName,
            'courseDes': courseDes,
            'volume': volume,
        }
        console.log(data);
        if (gradeId == '0' || gradeId == '' || gradeId == undefined) {
            $('#errorTips').removeClass('hidden').find('strong').text('请选择年级');
        }
        else if (volume == '0' || volume == '' || volume == undefined) {
            $('#errorTips').removeClass('hidden').find('strong').text('请选择上下册');
        }
        else if (courseName == '' || courseName == undefined) {
            $('#errorTips').removeClass('hidden').find('strong').text('课程名不能为空');
        }
        else {
            $.ajax({
                type: 'POST',
                url: '/courseManage/',
                data: data,
                headers: {
                    'X-CSRFToken': $.cookie('csrftoken')
                },
                async: false,
                err: function () {

                },
                success: function (callback) {
                    if (callback == 'success') {
                        window.location.href = "/courses/";
                    } else {
                        $('#errorTips').removeClass('hidden').find('strong').text(callback);
                    }
                }
            });
        }
    });
    $("#teacherEdit").on('click', function () {
        var userName = $("#UserName").val();
        var password = $("#Password").val();
        var id = $('#teacherId').val();
        var repassword = $("#Password_confirmation").val();
        var pwdpattern = /^(?![0-9]+$)(?![a-zA-Z]+$)[0-9A-Za-z]{6,21}$/;
        var userNamePattern = /^[a-zA-Z0-9_]{4,12}$/;
        var step = 0;
        if (step == 0) {
            if (userName == "" || userName == null) {
                danger("errorTips", "用户名不能为空");
            }
            else if (userNamePattern.test(userName) == false) {
                danger("errorTips", "用户名长度限制为4-12位,可包含字母，数字，下划线");
            }
            else {
                $("#errorTips").addClass("hidden");
                step = 1;
            }
        }
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
                url: "/teacherManage/",
                data: { username: userName, password: repassword, id:id },
                headers: {
                    'X-CSRFToken': $.cookie('csrftoken')
                },
                async: true,
                error: function (request) {
                    danger("errorTips", "对不起，注册失败，请稍后重新注册。");
                },
                success: function (callback) {
                    if(callback == 'success'){
                        window.location.href = '/teachers/';
                    }else{
                        danger("errorTips", callback);
                    }
                }
            });
        }
    });
    $("#myStudentEdit").on('click', function () {
        var userName = $("#UserName").val();
        var password = $("#Password").val();
        var id = $('#studentId').val();
        var repassword = $("#Password_confirmation").val();
        var pwdpattern = /^(?![0-9]+$)(?![a-zA-Z]+$)[0-9A-Za-z]{6,21}$/;
        var userNamePattern = /^[a-zA-Z0-9_]{4,12}$/;
        var step = 0;
        if (step == 0) {
            if (userName == "" || userName == null) {
                danger("errorTips", "用户名不能为空");
            }
            else if (userNamePattern.test(userName) == false) {
                danger("errorTips", "用户名长度限制为4-12位,可包含字母，数字，下划线");
            }
            else {
                $("#errorTips").addClass("hidden");
                step = 1;
            }
        }
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
                url: "/myStudentManage/",
                data: { username: userName, password: repassword, id:id },
                headers: {
                    'X-CSRFToken': $.cookie('csrftoken')
                },
                async: true,
                error: function (request) {
                    danger("errorTips", "对不起，注册失败，请稍后重新注册。");
                },
                success: function (callback) {
                    if(callback == 'success'){
                        window.location.href = '/myStudents/';
                    }else{
                        danger("errorTips", callback);
                    }
                }
            });
        }
    });

}).call(this);