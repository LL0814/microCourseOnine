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
})

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
