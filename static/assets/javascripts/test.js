function ajax_query(taskName, type) {
    $.ajax({
        type: "POST",
        url: "/addTestPaper/",
        data: { 'taskName': taskName, 'type': type, 'action': 'query' },
        headers: {
            'X-CSRFToken': $.cookie('csrftoken')
        },
        async: true,
        error: function (request) {
        },
        success: function (feedback) {
            console.log(feedback);
            if (feedback && feedback.length > 0) {
                if(type == 1) {
                    appendSingleQueryResult(feedback);
                }
                else if(type == 2) {
                    appendMultipleQueryResult(feedback);
                }
                else if(type == 3) {
                    appendCheckQueryResult(feedback);
                }
                else if(type == 4) {
                    appendFillInQueryResult(feedback);
                }
            }
            else {
                if(type == 1) {
                    clearSingleQueryResult();
                }
                else if(type == 2){
                    clearMultipleQueryResult();
                }
                else if(type == 3){
                    clearCheckQueryResult();
                }
                else if(type == 4){
                    clearFillInQueryResult();
                }
            }
        }
    });
}
function ajax_submit_test_paper(testPaperName, tasks, scores, score_count) {
    $.ajax({
        type: "POST",
        url: "/addTestPaper/",
        data: { 'testPaperName': testPaperName, 'tasks': tasks, 'score_count': score_count, 'scores':scores, 'action':'submit' },
        headers: {
            'X-CSRFToken': $.cookie('csrftoken')
        },
        async: true,
        error: function (request) {
        },
        success: function (id) {
            window.location.href = '/testPaperDetail/' + id;
        }
    });
}
function appendSingleQueryResult(feedback){
    $('.dynamic-query-result ul').empty();
    feedback.map((task) => {
        $('.dynamic-query-result ul').append("<li id='task-" + task.id +"'> \
        <button class='btn btn-primary btn-small btn-singe-add' type='button'>\<i class='icon-plus'></i></button>\
        <span class='test-task-name'>" + task.name + "</span>\
        <span class='test-alternativeAnswers-container hidden'>"+task.alternativeAnswers+"</span>\
        <span class='test-standardAnswers-container hidden'>"+task.standardAnswers+"</span></li>");
    });
}
function clearSingleQueryResult() {
    $('.dynamic-query-result ul').empty().append("<span style='color: #777;'>没有查找到相关题目... <span>");
}
function appendMultipleQueryResult(feedback){
    $('.dynamic-multiple-query-result ul').empty();
    feedback.map((task) => {
        $('.dynamic-multiple-query-result ul').append("<li id='task-" + task.id +"'> \
        <button class='btn btn-primary btn-small btn-multiple-add' type='button'>\<i class='icon-plus'></i></button>\
        <span class='test-task-name'>" + task.name + "</span>\
        <span class='test-alternativeAnswers-container hidden'>"+task.alternativeAnswers+"</span>\
        <span class='test-standardAnswers-container hidden'>"+task.standardAnswers+"</span></li>");
    });
}
function clearMultipleQueryResult() {
    $('.dynamic-multiple-query-result ul').empty().append("<span style='color: #777;'>没有查找到相关题目... <span>");
}
function appendCheckQueryResult(feedback){
    $('.dynamic-check-query-result ul').empty();
    feedback.map((task) => {
        $('.dynamic-check-query-result ul').append("<li id='task-" + task.id +"'> \
        <button class='btn btn-primary btn-small btn-check-add' type='button'>\<i class='icon-plus'></i></button>\
        <span class='test-task-name'>" + task.name + "</span>\
        <span class='test-alternativeAnswers-container hidden'>"+task.alternativeAnswers+"</span>\
        <span class='test-standardAnswers-container hidden'>"+task.standardAnswers+"</span></li>");
    });
}
function clearCheckQueryResult() {
    $('.dynamic-check-query-result ul').empty().append("<span style='color: #777;'>没有查找到相关题目... <span>");
}
function appendFillInQueryResult(feedback){
    $('.dynamic-fillIn-query-result ul').empty();
    feedback.map((task) => {
        $('.dynamic-fillIn-query-result ul').append("<li id='task-" + task.id +"'> \
        <button class='btn btn-primary btn-small btn-fillIn-add' type='button'>\<i class='icon-plus'></i></button>\
        <span class='test-task-name'>" + task.name + "</span>\
        <span class='test-alternativeAnswers-container hidden'>"+task.alternativeAnswers+"</span>\
        <span class='test-standardAnswers-container hidden'>"+task.standardAnswers+"</span></li>");
    });
}
function clearFillInQueryResult() {
    $('.dynamic-fillIn-query-result ul').empty().append("<span style='color: #777;'>没有查找到相关题目... <span>");
}

$('#btn-test-header').on('click', function(){
    let test_date_grade = $('.test-date-grade').text();
    let test_course_name = $('.test-course-name').text();
    let test_score_time = $('.test-score-time').text();
    $('#test-date-grade').val(test_date_grade);
    $('#test-course-name').val(test_course_name);
    $('#test-score-time').val(test_score_time);
});
$('#test-header-save').on('click', function() {
    let test_date_grade = $('#test-date-grade').val();
    let test_course_name = $('#test-course-name').val();
    let test_score_time = $('#test-score-time').val();
    $('.test-date-grade').text(test_date_grade);
    $('.test-course-name').text(test_course_name);
    $('.test-score-time').text(test_score_time);
});
$('#test-singe-task-query').bind('input propertychange', function() {
    $('.dynamic-query-result ul').empty().append("<img alt='11' src='/static/assets/images/ajax-loaders/11.gif' />")
    let input_val = $(this).val();
    console.log(input_val);
    ajax_query(input_val, 1);
});
$('#test-multiple-task-query').bind('input propertychange', function() {
    $('.dynamic-query-multiple-result ul').empty().append("<img alt='11' src='/static/assets/images/ajax-loaders/11.gif' />")
    let input_val = $(this).val();
    console.log(input_val);
    ajax_query(input_val, 2);
});
$('#test-check-query').bind('input propertychange', function() {
    $('.dynamic-check-query-result ul').empty().append("<img alt='11' src='/static/assets/images/ajax-loaders/11.gif' />")
    let input_val = $(this).val();
    console.log(input_val);
    ajax_query(input_val, 3);
});
$('#test-fillIn-query').bind('input propertychange', function() {
    $('.dynamic-fillIn-query-result ul').empty().append("<img alt='11' src='/static/assets/images/ajax-loaders/11.gif' />")
    let input_val = $(this).val();
    console.log(input_val);
    ajax_query(input_val, 4);
});

$("#test-container").on('click', '.box-remove', function(){
    $(this).parentsUntil('.row-fluid').remove();
});
$(".dynamic-query-result").on('click', '.btn-singe-add', function(){
    let name;
    let alternativeAnswers;
    let standardAnswers;
    let id;
    let taskContent;
    var thisLen;
    id = $(this).parent().attr('id');
    $(this).nextAll().map((index, dom) => {
        var value =$(dom).text();
        if(index == 0) {
            name = value;
        } else if(index == 1) {
            alternativeAnswers = value.split('&&&');
        }
        else {
            standardAnswers = value;
        }
    })
    console.log(id , name, alternativeAnswers, standardAnswers);
    var content = "";
    alternativeAnswers.map( (answer, index, array) => {
        var temple;
        console.log(answer, index, array);
        if(index == standardAnswers) {
            temple = "<ul><input type='radio' name='"+id+"answer' checked><label>" + answer + "</label><br/></ul>";
        }
        else {
            temple = "<ul><input type='radio' name='"+id+"answer'><label>" + answer + "</label><br/></ul>";
        }
        content += temple;
    });
    
    taskContent = "<div class='row-fluid' id='"+ id +"'>\
        <div class='span12 box'>\
            <div class='box-header'>\
                <div class='actions'>\
                    <a href='#' class='btn box-remove btn-mini btn-link'><i class='icon-remove'></i>\</a>\
                </div>\
            </div>\
            <div class='box-content'>\
                <div class='accordion accordion-blue' style='margin-bottom:0;'>\
                    <div class='accordion-group'>\
                        <div class='accordion-heading'>\
                            <span class='accordion-toggle'>"+ name +"</span>\
                        </div>\
                        <div class='accordion-body'>\
                            <div class='accordion-inner answer'>"+ content +"</div>\
                            <input class='task-score' type='number' value='5'/>\
                        </div>\
                    </div>\
                </div>\
            </div>\
        </div>\
    </div>";
    thisRes = $("div[id='"+id+"']");
    thisLen = thisRes.length;
    if(thisLen == 0)
    {
        $('#test-container').append(taskContent);
    }
});
$(".dynamic-multiple-query-result").on('click', '.btn-multiple-add', function(){
    let name;
    let alternativeAnswers;
    let standardAnswers;
    let id;
    let taskContent;
    id = $(this).parent().attr('id');
    $(this).nextAll().map((index, dom) => {
        var value =$(dom).text();
        if(index == 0) {
            name = value;
        } else if(index == 1) {
            alternativeAnswers = value.split('&&&');
        }
        else {
            standardAnswers = value.split('&&&');
        }
    })
    console.log(id , name, alternativeAnswers, standardAnswers);
    var content = "";
    alternativeAnswers.map( (answer, index, array) => {
        var temple;
        console.log(answer, index, array);
        if(standardAnswers.indexOf(''+index) != -1) {
            temple = "<ul><input type='checkbox' name='"+id+"answer' checked><label>" + answer + "</label><br/></ul>";
        }
        else {
            temple = "<ul><input type='checkbox' name='"+id+"answer'><label>" + answer + "</label><br/></ul>";
        }
        content += temple;
    });
    
    taskContent = "<div class='row-fluid' id='"+ id +"'>\
        <div class='span12 box'>\
            <div class='box-header'>\
                <div class='actions'>\
                    <a href='#' class='btn box-remove btn-mini btn-link'><i class='icon-remove'></i>\</a>\
                </div>\
            </div>\
            <div class='box-content'>\
                <div class='accordion accordion-red' style='margin-bottom:0;'>\
                    <div class='accordion-group'>\
                        <div class='accordion-heading'>\
                            <span class='accordion-toggle'>"+ name +"</span>\
                        </div>\
                        <div class='accordion-body'>\
                            <div class='accordion-inner answer'>"+ content +"</div>\
                            <input class='task-score' type='number' value='5'/>\
                        </div>\
                    </div>\
                </div>\
            </div>\
        </div>\
    </div>";
    if($("div[id='"+id+"']").length == 0)
    {
        $('#test-container').append(taskContent);
    }
});
$(".dynamic-check-query-result").on('click', '.btn-check-add', function(){
    let name;
    let alternativeAnswers;
    let standardAnswers;
    let id;
    let taskContent;
    id = $(this).parent().attr('id');
    $(this).nextAll().map((index, dom) => {
        var value =$(dom).text();
        if(index == 0) {
            name = value;
        } else if(index == 1) {
            alternativeAnswers = value.split('&&&');
        }
        else {
            standardAnswers = value.split('&&&');
        }
    })
    console.log(id , name, alternativeAnswers, standardAnswers);
    var content = "";
    if(standardAnswers == 0) {
        content = "<ul><input type='radio' name='"+ id +"answer' value='0' checked> <label>错误</label><br/><input type='radio' name='answer' value='1'> <label>正确</label><br/></ul>";
    }
    else {
        content = "<ul><input type='radio' name='"+ id +"answer' value='0'> <label>错误</label><br/><input type='radio' name='answer' value='1' checked> <label>正确</label><br/></ul>"
    }
    
    taskContent = "<div class='row-fluid' id='"+ id +"'>\
        <div class='span12 box'>\
            <div class='box-header'>\
                <div class='actions'>\
                    <a href='#' class='btn box-remove btn-mini btn-link'><i class='icon-remove'></i>\</a>\
                </div>\
            </div>\
            <div class='box-content'>\
                <div class='accordion accordion-green' style='margin-bottom:0;'>\
                    <div class='accordion-group'>\
                        <div class='accordion-heading'>\
                            <span class='accordion-toggle'>"+ name +"</span>\
                        </div>\
                        <div class='accordion-body'>\
                            <div class='accordion-inner answer'>"+ content +"</div>\
                            <input class='task-score' type='number' value='5'/>\
                        </div>\
                    </div>\
                </div>\
            </div>\
        </div>\
    </div>";
    if($("div[id='"+id+"']").length == 0)
    {
        $('#test-container').append(taskContent);
    }
});
$(".dynamic-fillIn-query-result").on('click', '.btn-fillIn-add', function(){
    let name;
    let id;
    let taskContent;
    let standardAnswers;
    id = $(this).parent().attr('id');
    $(this).nextAll().map((index, dom) => {
        var value =$(dom).text();
        if(index == 0) {
            name = value;
        }
        else if(index == 2) {
            standardAnswers = value;
        }
    })
    var content = "<input class='input-block-level' value='"+ standardAnswers +"' />";
    taskContent = "<div class='row-fluid' id='"+ id +"'>\
        <div class='span12 box'>\
            <div class='box-header'>\
                <div class='actions'>\
                    <a href='#' class='btn box-remove btn-mini btn-link'><i class='icon-remove'></i>\</a>\
                </div>\
            </div>\
            <div class='box-content'>\
                <div class='accordion accordion-purple' style='margin-bottom:0;'>\
                    <div class='accordion-group'>\
                        <div class='accordion-heading'>\
                            <span class='accordion-toggle'>"+ name +"</span>\
                        </div>\
                        <div class='accordion-body'>\
                            <div class='accordion-inner answer'>"+ content +"</div>\
                            <input class='task-score' type='number' value='5'/>\
                        </div>\
                    </div>\
                </div>\
            </div>\
        </div>\
    </div>";
    if($("div[id='"+id+"']").length == 0)
    {
        $('#test-container').append(taskContent);
    }
});
$("#test-container").on('click', '.task-score', function(){
    score = $(this).val();
    if(score <= 0 || score == '' || score === undefined) {
        $(this).css('color', 'red');
    }
    else{
        $(this).css('color', '');
    }
});
$('#submit-test-paper').on('click', function(){
    let flag = 0;
    let score_count = 0;
    let task_list = new Array();
    let score_list = new Array();
    let testPaperName;
    var reg = /^[0-9]*[1-9][0-9]*$/　　//正整数 
    $('.task-score').map((index, tsk) => {
        let task = $(tsk);
        let score = task.val();
        if(!reg.test(score)) {
            task.css('color', 'red');
            flag ++;
        }
        else{
            score_count += parseInt(score);
            score_list.push(parseInt(score));
        }
    });
    if(flag > 0) {
        $('#errorTips').removeClass('hidden').text('请输入正确的分值');
    }
    else {
        $('#errorTips').addClass('hidden')
        $("div[id^='task-']").map((index, task) => {
            task_list.push($("div[id^='task-']")[index].id.replace('task-', ''));
        })
    }
    let tasks = task_list.join('&&&');
    let scores = score_list.join('&&&');
    testPaperName = $('.test-date-grade').text() + '&&&' + $('.test-course-name').text() + '&&&' + $('.test-score-time').text();
    ajax_submit_test_paper(testPaperName, tasks, scores, score_count);
});
$('#submit-test').on('click', function() {
    let curl = window.location.href;
    $.ajax({
        type: "POST",
        url: curl,
        data: {'url': curl,},
        headers: {
            'X-CSRFToken': $.cookie('csrftoken')
        },
        async: true,
        error: function (err) {
        },
        success: function (feedback) {
            if(feedback == 'ok') {
                window.location.href = '/myTests/';   
            }
            else {
                danger("error_tips", feedback);
            }
        }
    });
})

$('.test-change-status').on('click', function() {
    let ths = $(this);
    let testDetail = $(this).parentsUntil('tbody').children();
    let testDetailUrl = testDetail.find('a').attr('href');
    $.ajax({
        type: "POST",
        url: '/myTests/',
        data: {'url': testDetailUrl,},
        headers: {
            'X-CSRFToken': $.cookie('csrftoken')
        },
        async: true,
        error: function (err) {
        },
        success: function (feedback) {
            if(feedback == 'start') {
                let td =testDetail[3];
                $(td).text('进行中');
                ths.text('结束');
            }
            else {
                let td =testDetail[3];
                $(td).text('未激活');
                ths.text('开始');
            }
        }
    });
})