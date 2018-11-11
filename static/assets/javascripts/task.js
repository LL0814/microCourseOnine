function danger(tid, tips) {
    $("#" + tid).removeClass('hidden').text(tips);
}
function removeTips(tid) {
    $("#" + tid).addClass("hidden");
}
function ajax_submit(taskId, question, standardAnswer, alternativeAnswers, type) {
    $.ajax({
        type: "POST",
        url: "/myTaskManage/",
        data: { 'id': taskId, 'name': question, 'standardAnswer': standardAnswer, 'alternativeAnswers': alternativeAnswers, 'type': type },
        headers: {
            'X-CSRFToken': $.cookie('csrftoken')
        },
        async: true,
        error: function (request) {
            danger("error_tips", "对不起，新建或者更新失败，请稍后再试。");
        },
        success: function (callback) {
            if (callback == 'success') {
                window.location.href = '/myTasks/';
            } else {
                danger("error_tips", callback);
            }
        }
    });
}
$(".answer").on('click', '#addSinglePicklistOption', function () {
    $('#addSinglePicklistOption').prev().append('<input type="radio" name="answer"><label><input type="text" name="alternativeAnswer" value="" placeholder="请输入备选答案..."/></label><br/>');
});
$(".answer").on('click', '#addMultiplePicklistOption', function () {
    $('#addMultiplePicklistOption').prev().append('<input type="checkbox" name="answer"><label><input type="text" name="alternativeAnswer" value="" placeholder="请输入备选答案..."/></label><br/>');
});
$("#taskType").on('change', function () {
    var option = $('#taskType').find("option:selected").text();
    $('.answer').empty();
    if (option == "单选题") {
        $('.answer').append("<ul><input type='radio' name='answer'> <label><input type='text' name='alternativeAnswer' placeholder='例: A. 今天星期几？'/></label><br/></ul><button id='addSinglePicklistOption' type='button' class='btn btn-primary btn-small'>添加备选答案</button>");
    }
    else if (option == "多选题") {
        $('.answer').append("<ul><input type='checkbox' name='answer'> <label><input type='text' name='alternativeAnswer' placeholder='例: A. 今天星期几？'/></label><br/></ul><button id='addMultiplePicklistOption' type='button' class='btn btn-primary btn-small'>添加备选答案</button>");
    }
    else if (option == "判断题") {
        $('.answer').append("<ul><input type='radio' name='answer' value='1'> <label>正确</label><br/><input type='radio' name='answer' value='0'> <label>错误</label><br/></ul>");
    }
    else if (option == "填空题") {
        $('.answer').append("<input type='text' name='answer' placeholder='请输入标准答案...' />");
    }
    else {

    }
});
$("#taskEdit").on('click', function () {

    removeTips("error_tips");
    var selectedValue = $('#taskType').val();
    var taskName = $('#taskName').val();
    var selectedAnswer = $('input[name="answer"]:checked').val();
    var taskId = $('#taskId').val();
    if (selectedValue == 0) {
        danger("error_tips", "请选择题目类型");
    }
    else if (taskName == "") {
        danger("error_tips", "请输入题目内容");
    }
    else if (selectedValue == 4) { //填空题
        var standardAnswer = $("input[name='answer']").val();
        if (standardAnswer == "") {
            danger("error_tips", "请输入标准答案");
        } else {
            //SUBMIT
            ajax_submit(taskId, taskName, standardAnswer, '', 4);
        }
    }
    else if (selectedAnswer === undefined) {
        danger("error_tips", "请选择标准答案");
    }
    else if (selectedValue == 3) { //判断题
        var standardAnswer = new Array();
        $("[name='answer']").map((index) => {
            if($("[name='answer']")[index].checked) {
                standardAnswer.push(index);
            }
        });
        standardAnswer = standardAnswer.join('&&&');
        //submit
        ajax_submit(taskId, taskName, standardAnswer, '', 3);
    }
    else if (selectedValue == 1) { //单选题
        var standardAnswer = new Array();
        var alternativeAnswers = new Array();
        $("[name='answer']").map((index) => {
            if($("[name='answer']")[index].checked) {
                standardAnswer.push(index);
            }
        })
        $("input[name='alternativeAnswer']").each(function () {
            alternativeAnswers.push($(this).val());
        })
        alternativeAnswers = alternativeAnswers.join('&&&');
        standardAnswer = standardAnswer.join('&&&');
        //submit

        ajax_submit(taskId, taskName, standardAnswer, alternativeAnswers, 1);
    }
    else if (selectedValue == 2) { //多选题
        var standardAnswer = new Array();
        var alternativeAnswers = new Array();
        $("[name='answer']").map((index) => {
            if($("[name='answer']")[index].checked) {
                standardAnswer.push(index);
            }
        });
        $("input[name='alternativeAnswer']").each(function () {
            alternativeAnswers.push($(this).val());
        })
        alternativeAnswers = alternativeAnswers.join('&&&')
        standardAnswer = standardAnswer.join('&&&');
        ajax_submit(taskId, taskName, standardAnswer, alternativeAnswers, 2);
    }
});
window.onload = function() {
    let type = $("#task_type").val();
    let standardAnswers = $("#task_standardAnswers").val();
    let alternativeAnswers = $("#task_alternativeAnswers").val().split('&&&');
    $("#taskType").val(type);
    if(type == 4) {
        $(".task-type-label").text('填空题');
        $('.answer').append("<input type='text' name='answer' value =" + standardAnswers + " placeholder='请输入标准答案...' />");
    }
    if(type == 3) {
        $(".task-type-label").text('判断题');
        if(standardAnswers == 0) {
            html = "<ul><input type='radio' name='answer' value='0' checked> <label>错误</label><br/><input type='radio' name='answer' value='1'> <label>正确</label><br/></ul>";
        }
        else {
            html = "<ul><input type='radio' name='answer' value='0'> <label>错误</label><br/><input type='radio' name='answer' value='1' checked> <label>正确</label><br/></ul>"
        }
        $('.answer').append(html);
    }
    if(type == 2) {
        $(".task-type-label").text('多选题');
        var html = "";
        var button = "<button id='addMultiplePicklistOption' type='button' class='btn btn-primary btn-small'>添加备选答案</button>";
        standardAnswers = standardAnswers.split('&&&');
        alternativeAnswers.map( (answer, index, array) => {
            var temple;
            if(standardAnswers.indexOf(''+index) != -1) {
                console.log(index);
                temple = "<ul><input type='checkbox' name='answer' checked> <label><input type='text' name='alternativeAnswer' value=" + answer + " placeholder='例: A. 今天星期几？'/></label><br/></ul>";
            }
            else {
                temple = "<ul><input type='checkbox' name='answer'> <label><input type='text' name='alternativeAnswer' value=" + answer + " placeholder='例: A. 今天星期几？'/></label><br/></ul>";
            }
            html += temple;
        });
        html += button;
        $('.answer').append(html);
    }
    if(type == 1) {
        $(".task-type-label").text('单选题');
        var html = "";
        var button = "<button id='addSinglePicklistOption' type='button' class='btn btn-primary btn-small'>添加备选答案</button>";
        alternativeAnswers.map( (answer, index, array) => {
            var temple;
            console.log(answer, index, array);
            if(index == standardAnswers) {
                temple = "<ul><input type='radio' name='answer' checked> <label><input type='text' name='alternativeAnswer' value=" + answer + " placeholder='例: A. 今天星期几？'/></label><br/></ul>";
            }
            else {
                temple = "<ul><input type='radio' name='answer'> <label><input type='text' name='alternativeAnswer' value=" + answer + " placeholder='例: A. 今天星期几？'/></label><br/></ul>";
            }
            html += temple;
        });
        html += button;
        $('.answer').append(html);
    }
} 