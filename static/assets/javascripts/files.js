$('#getUnitCourses').on('click', function() {
    let gradeId = Number($('#select-grade').val());
    let gradeName = $("#select-grade").find("option:selected").text(); 
    let courseId = Number($('#select-course').val());
    let courseName = $("#select-course").find("option:selected").text();
    if(!gradeId || gradeId == 0){
        danger("errorTips", "请选择年级");
    }
    else if(!courseId || courseId == 0){
        danger("errorTips", "请选择课程类别");
    }
    else
    {
        removeTips('errorTips');
        $.ajax({
            type: "POST",
            url: "/selectUnit/",
            data: {
                'gradeId': gradeId,
                'courseId': courseId,
                'action':'getUnits' },
            headers: {
                'X-CSRFToken': $.cookie('csrftoken')
            },
            async: true,
            error: function (request) {
                danger("errorTips", "对不起, 编辑失败, 请稍后再试");
            },
            success: function (callback) {
                let rows = '';
                callback.map((unit) =>{
                    rows += "<tr><td><a href='/UnitCourseManage/" + unit.id +"'>" + unit.name + "</a></td><td>" + unit.description + "</td></tr>";
                })
                $('#unit-items').empty();
                $('#unit-items').append(rows);
                $('.unit-items-title').text(gradeName + '  ' + courseName);
                $('.unit-items-container').removeClass('hidden');
            }
        });
    }
})