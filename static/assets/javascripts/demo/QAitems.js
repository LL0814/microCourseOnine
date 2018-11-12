    /*123*/
    /*管理员-wiki-删除*/
    function admin_wiki_del(){
        layer.confirm('确认要删除该动态吗？',function(){
            var  curl= window.location.href;
            $.ajax({
                type: "POST",
                url: curl,
                data:{"addr":"del","url":curl},
                headers: {
                    'X-CSRFToken': $.cookie('csrftoken')
                },
                async: false,
                error: function (request) {
                    layer.msg('删除失败!',{icon:6,time:600});
                },
                success: function (data) {
                    layer.msg('删除成功!',{icon:6,time:600});
                    window.location.href = "/QA/"
                }
            });
        });
    }
    //加载页面，创建编辑器
    $(function(){
        var editor = KindEditor.create("#commenteditor",{
            width:"96%",
            height:"100px",
            autoHeightMode:true,
            extraFileUploadParams:{
                csrfmiddlewaretoken:$.cookie('csrftoken')
            },
            items:[
                'undo', 'redo' ,'|', 'preview','|', 'forecolor', 'hilitecolor', 'bold',
                'italic', 'underline', '|', 'image',  'emoticons', 'link','|'
            ],
            uploadJson:'/upload_imgs/'
        });
    
        var  curl= window.location.href;
        $("#answer-submit").on('click',function(){
            html = editor.html();
            if(html == ""){
                $("#error_tips").text("*内容不能为空").removeClass('hidden');
            }
            else 
            {
                $("#error_tips").text("");
                $.ajax({
                type: "POST",
                url: curl,
                data:{"answer":html,'url':curl,},
                headers: {
                    'X-CSRFToken': $.cookie('csrftoken')
                },
                async: true,
                error: function (request) {
                    $("#error_tips").text("*发生了一个预期之外的错误,请联系管理员!").removeClass('hidden');
                },
                success: function (callback) {
                    if(callback == 'success')
                    {
                        window.location.reload(true);
                    }
                    else
                    {
                        $("#error_tips").text("*发生了一个预期之外的错误,请联系管理员!").removeClass('hidden');
                    }
                    
                }
            });
        }
    });
});
    function showcomment(ths) {

        if(ths.value == 1){
            document.getElementById("sc").style.display = "block";
            ths.value = 0;
        }
        else{
            document.getElementById("sc").style.display = "none";
            ths.value = 1;
        }
    }