
//display the error messeges
function danger(tid,tips){
	$("#"+tid).removeClass("hidden").removeClass("alert-success").addClass("alert-danger").text(tips);
}

//dispaly the sucessful messeges
function success(tid,tips){
	$("#"+tid).removeClass("hidden").removeClass("alert-danger").addClass("alert-success").text(tips);
}

//verify if the input value is blank
function verifyInputValueIsBlank(ths,bid,tid){
	if( ths.value == "" || ths.value == null ){
		var tips = ths.placeholder + "不能为空";
		danger(tid,tips);
		$("#"+bid).attr("disabled","disabled");
	}else {
		$("#"+tid).addClass("hidden");
		$('#'+bid).removeAttr("disabled");
	}
};

//verify if two of the input value is blank
function verifyPwd(bid){
	if($("#passWord").val() != $("#rePassWord").val()){
		$(".tips").removeClass("hidden").removeClass("alert-success").addClass("alert-danger").text("两次密码不匹配.");
		$("#"+bid).attr("disabled","disabled");
	}else {
		$(".tips").addClass("hidden");
		$('#'+bid).removeAttr("disabled");
	}
};

function clearTips(){	
	var tid = 'warnings';
	$("#"+tid).addClass("hidden");
};

//sign in button logic
$("#signIn").click(function(){
	var userName = $("#UserName").val();
	var passWord = $("#Password").val();
	var remember = $("#remember").is(":checked");
	if(userName == "" || userName == null) {
		danger("warnings","用户名不能为空");
	}
	else if(passWord == "" || passWord == null) {
		danger("warnings","密码不能为空");
	}
	else {
		$.ajax({
			type: "POST",
			url: "/login/",
			data: {UserName: userName, Password:passWord, Remember:remember},
			headers: {
				'X-CSRFToken': $.cookie('csrftoken')
			},
			async: true,
			error: function (request) {
				danger("服务器错误，请稍后再试.");
			},
			success: function (data) {
				if(data == "用户名或密码错误"){
					danger("warnings","用户名或密码错误");
				}
				else{
					window.location.href = data;
				}
			}
		});
	}
});

//sign up page button logic
$("#signUp").click(function(){
	var userName = $("#UserName").val();
	var password = $("#Password").val();
	var repassword = $("#Password_Confirmation").val();
	var pwdpattern = /^(?![0-9]+$)(?![a-zA-Z]+$)[0-9A-Za-z]{6,21}$/;
	var userNamePattern = /^[a-zA-Z0-9_]{4,12}$/;
	var step = 0;
	if(step == 0)
	{
		if(userName == "" || userName == null) {
			danger("warnings","用户名不能为空");
		}
		else if(userNamePattern.test(userName) == false){
			danger("warnings","用户名长度限制为4-12位,可包含字母，数字，下划线");
		}
		else{
			$("#warnings").addClass("hidden");
			step = 1;
		}
	}
	if(step == 1)
	{
		if(password == "" || password == null) {
			danger("warnings","密码不能为空");
		}
		else{
			step = 2;
		}
	}
	if(step == 2)
	{
		if(pwdpattern.test(password) == false){
			danger("warnings","密码由6-21字母和数字组成，不能是纯数字或纯英文");
		}
		else{
			step = 3;
		}
	}
	if(step == 3)
	{
		if(password != repassword)
		{
			danger("warnings","两次密码不匹配");
		}
		else{
			step = 4;
		}
	}
	if(step == 4){
		$.ajax({
			type: "POST",
			url: "/signUp/",
			data: {UserName:userName, Password: repassword},
			headers: {
				'X-CSRFToken': $.cookie('csrftoken')
			},
			async: true,
			error: function (request) {
				danger("warnings","对不起，注册失败，请稍后重新注册。")
			},
			success: function (data) {
				if(data == "unIsBlank"){
					danger("warnings","用户名不能为空");
				}
				else if(data == "pwIsBlank"){
					danger("warnings","密码不能为空");
				}
				else if(data == "unIsExist"){
					danger("warnings","用户名已存在");
				}
				else if(data == "err"){
					danger("warnings","注册失败，请稍后再试.");
				}
				else{
					success("warnings","注册成功.");
					setTimeout(function(){
						window.location.href = '/index/';
					},2000);
				}
			}
		});
	}
});

//reset password page buttons logic
$("#form1Button").click(function(){
	var mailaddress = $("#form1Email").val();
	var checkcode = $("#form1CheckCode").val();
	if(mailaddress == "" || mailaddress == null) {
		danger("form1Warnings","邮箱不能为空");
		$("#form1Button").attr("disabled","disabled");
	}
	else if(checkcode == "" || checkcode == null) {
		danger("form1Warnings","验证码不能为空");
		$("#form1Button").attr("disabled","disabled");
	}
	else {
		$("#form1").addClass("hidden");
		$("#form2").removeClass("hidden");
		success("form2Tips","正在发送邮件...");
		$("#form2Buttom").addClass("hidden");
		$.ajax({
			type: "POST",
			url: "/reset/",
			data: {email: mailaddress,identify_code:checkcode},
			headers: {
				'X-CSRFToken': $.cookie('csrftoken')
			},
			async: true,
			error: function (request) {
				danger("form2Tips","对不起，邮件发送失败，请稍后再试。。。")
			},
			success: function (data) {
				var str = "0123456789";
					var n = 11, s = "";
					for(var i = 0; i < n; i++){
						var rand = Math.floor(Math.random() * str.length);
						s += str.charAt(rand);
					}
				if(data == "false"){
					danger("form2Tips","验证码错误");
					$("#form2Buttom").addClass("hidden");
					$("#form2Sign").removeClass("hidden");
				}
				else if(data == "DoesNotExist"){
					danger("form2Tips","该邮箱尚未注册...");
					$("#form2Buttom").addClass("hidden");
					$("#form2Sign").removeClass("hidden");
				}
				else{
					success("form2Tips","邮件发送成功，请及时查看邮件获取验证码，有效期，2小时...");
					$("#form2Sign").addClass("hidden");
					$("#form2Buttom").removeClass("hidden");
				}
			}
		});
	}
});

$("#form2Buttom").click(function(){
	$("#form2").addClass("hidden");
	$("#form3").removeClass("hidden");
});

$("#form3Button").click(function(){
	var mailaddress = $("#form3Email").val();
	var mailcode = $("#form3VerifykCode").val();
	var password = $("#passWord").val();
	var repassword = $("#rePassWord").val();
	var pwdpattern = /^(?![0-9]+$)(?![a-zA-Z]+$)[0-9A-Za-z]{6,21}$/;
	var pattern = /^\d{5,12}@[qQ1][qQ6]3?\.(com|cn)$/;
	var step = 0;
	if(step == 0)
	{
		if(mailaddress == "" || mailaddress == null) {
			danger("form3Tips","邮箱不能为空");
			$("#form3Button").attr("disabled","disabled");
		}
		else if(pattern.test(mailaddress) == false){
			danger("form3Tips","邮箱格式不正确");
			$("#form3Button").attr("disabled","disabled");
		}
		else{
			$("#form3Tips").addClass("hidden");
			$('#form3Button').removeAttr("disabled");
			step = 1;
		}
	}
	if(step == 1)
	{
		if(password == "" || password == null) {
			danger("form3Tips","密码不能为空");
			$("#form3Button").attr("disabled","disabled");
		}
		else{
			$("#form3Tips").addClass("hidden");
			$('#form3Button').removeAttr("disabled");
			step = 2;
		}
	}
	if(step == 2)
	{
		if(pwdpattern.test(password) == false){
			danger("form3Tips","密码由6-21字母和数字组成，不能是纯数字或纯英文");
			$("#form3Button").attr("disabled","disabled");
		}
		else{
			$("#form3Tips").addClass("hidden");
			$('#form3Button').removeAttr("disabled");
			step = 3;
		}
	}
	if(step == 3)
	{
		if(password != repassword)
		{
			danger("form3Tips","两次密码不匹配");
			$("#form3Button").attr("disabled","disabled");
		}
		else{
			$("#form3Tips").addClass("hidden");
			$('#form3Button').removeAttr("disabled");
			step = 4;
		}
	}
	if(step == 4)
	{
		if(mailcode == "" || mailcode == null) {
			danger("form3Tips","验证码不能为空");
			$("form3Button").attr("disabled","disabled");
		}
		else{
			$("#form3Tips").addClass("hidden");
			$('#form3Button').removeAttr("disabled");
			step = 5;
		}
	}
	if(step == 5){
		$.ajax({
			type: "POST",
			url: "/reset/",
			data: {emailaddr:mailaddress,emailcode: mailcode,password:repassword},
			headers: {
				'X-CSRFToken': $.cookie('csrftoken')
			},
			async: true,
			error: function (request) {
			},
			success: function (data) {
				if(data == "code_error"){
					danger("form3Tips","验证码错误");
					$("#form3Button").attr("disabled","disabled");
				}
				if(data == "DoesNotExist"){
					danger("form3Tips","邮箱不存在");
					$("#form3Button").attr("disabled","disabled");
				}
				if(data == "resetsuccess"){
					$("#form3").addClass("hidden");
					$("#form4").removeClass("hidden");
				}
			}
		});
	}
});
