$("#video-upload").click(function(){
    type = $("#video-type").find("option:selected").text();
    auth = $("#video-auth").find("option:selected").text();
    title = $("#video-title").val();
    description = $("#video-description").val();
    videoSrc = $("#videoContainer").attr("src");
    if(type == "类型")
    {
        $("#newideoTips").text("*请选择类型")
    }
    else if(title == "")
    {
        $("#newideoTips").text("*标题不能为空")
    }
    else if(description == "")
    {
        $("#newideoTips").text("*描述不能为空")
    }
    else if(videoSrc == "")
    {
        $("#newideoTips").text("*请上传视频")
    }
    else 
    {
        $("#newideoTips").text("");
        var  curl= window.location.href;
        formData = {
            'type': type,
            'title': title,
            'auth': auth,
            'description': description,
            'src': videoSrc
        }
        console.log(formData);
        $.ajax({
            type:'POST',
            url: curl,
            data: formData,
            headers: {
                'X-CSRFToken': $.cookie('csrftoken')
            },
            async: true,
            success: function(res) {
                if(res == 'ok'){
                    window.location.href = "/circle/video/show/";
                }
                else{
                    alert("服务器错误，请稍后再试。。。");
                }
            }
        });


    }
})

$("#video-add").change(function(){
    var file = $("#newVideo")[0].files[0];
    if (file && /\.(ogg|MPEG4|WebM|mp4|AVI|rm|rmvb|flash|mid|qsv)$/i.test(file.name) ) {
         //读取视频数据
         formData = new FormData();
         formData.append("file", file);
         $.ajax({
            type:'POST',
            url: "/upload_videos/",
            data: formData,
            headers: {
                'X-CSRFToken': $.cookie('csrftoken')
            },
            processData: false,
            contentType: false,
            async: false,
            success: function(src) {
                $("#videoContainer").attr("src", "/static/video/videos/"+src);
                $("#video-new-wrapper").removeClass("hidden");
                //$("#video-add-wrapper").addClass("hidden");
            }
        })
    }
    else{
        alert("视频格式不正确，仅支持：.ogg| .mp4 | .avi | .rmvb | .flash | .mid | .qsv");
    }
})