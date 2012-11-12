$(function(){
	
	//order_confirm.html
	$("#order_confirm_submit").bind('click',function(){
		if($("#order_confirm_user_accont").val() < $("#order_confirm_user_payables").val()){
			alert("你的账户余额不足，请充值先！");
			return false;
		}else{
			return true;
		}
		
		
	});
})