var update_tips = function(tips, txt) {
	tips.text(txt).addClass("ui-state-highlight");
	setTimeout(function() {
		tips.removeClass("ui-state-highlight", 1500);
	}, 500);
};
// update_tips
var check_length = function(o, min, max) {
	if(o.val().length > max || o.val().length < min) {
		o.addClass("ui-state-error");
		return false;
	} else {
		return true;
	}
};
// check_length
var check_regexp = function(o, regexp) {
	if(!(regexp.test(o.val()) )) {
		o.addClass("ui-state-error");
		return false;
	} else {
		return true;
	}
};
// check_regexp
var check_email = function(o) {
	return check_regexp(o, /^((([a-z]|\d|[!#\$%&'\*\+\-\/=\?\^_`{\|}~]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])+(\.([a-z]|\d|[!#\$%&'\*\+\-\/=\?\^_`{\|}~]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])+)*)|((\x22)((((\x20|\x09)*(\x0d\x0a))?(\x20|\x09)+)?(([\x01-\x08\x0b\x0c\x0e-\x1f\x7f]|\x21|[\x23-\x5b]|[\x5d-\x7e]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(\\([\x01-\x09\x0b\x0c\x0d-\x7f]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]))))*(((\x20|\x09)*(\x0d\x0a))?(\x20|\x09)+)?(\x22)))@((([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])*([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])))\.)+(([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])*([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])))\.?$/i);
};
// check_email
var create_dlg_recharge = function() {
	$("#dlg_recharge").dialog({
		autoOpen : false,
		modal : true
	});
	$("#form_recharge").submit(function(event) {
		event.preventDefault();
		var vals = $(this).serialize();
		$.post("/activity/recharge/", vals, function(json) {
			$("#dlg_recharge").dialog("close");
			if(json['success'] != true)
				return;
			query = '#tabs-group-members table td:contains(' + json['member'] + ')~td:eq(4)';
			$(query).text(json['balance']);
		});
	});
};
// create_dlg_recharge
var create_dlg_add_activity = function() {
	$(".date-picker").datepicker({
		"dateFormat" : "yy-mm-dd"
	});
	$("#dlg_add_activity").dialog({
		autoOpen : false,
		modal : true
	});
	$("#form_add_activity").submit(function(event) {
		event.preventDefault();
		var vals = $(this).serialize();
		$.post("/activity/add_activity/", vals, function(json) {
			$("#dlg_add_activity").dialog("close");
			if(json['success'])
				show_group_detail(json['gid']);
			// console.debug(json['message']);
		});
		window.location.hash = "tabs-recent-activity";
	});
};
// create_dlg_add_activity
var create_dlg_chg_activity = function() {
	$(".date-picker").datepicker({
		"dateFormat" : "yy-mm-dd"
	});
	$("#dlg_chg_activity").dialog({
		autoOpen : false,
		modal : true
	});
	$("#form_chg_activity").submit(function(event) {
		event.preventDefault();
		var vals = $(this).serialize();
		$.post("/activity/chg_activity/", vals, function(json) {
			$("#dlg_chg_activity").dialog("close");
			if(json['success'])
				show_group_detail(json['gid']);
			// console.debug(json['message']);
		});
		window.location.hash = "tabs-recent-activity";
	});
};
// create_dlg_chg_activity
var create_dlg_apply = function() {
	$("#dlg_apply").dialog({
		autoOpen : false,
		modal : true
	});

	$("#form_apply").submit(function(event) {
		event.preventDefault();
		var vals = $(this).serialize();
		$.post("/activity/apply_activity/", vals, function(data) {
			$("#dlg_apply").dialog("close");
			$(".ui-layout-center").html(data);
			decorate_group_detail();
		});
		window.location.hash = "tabs-recent-activity";
	});
};
// create_dlg_apply
var create_dlg_group_apply = function() {
	$("#dlg_group_apply").dialog({
		autoOpen : false,
		modal : true
	});

	$("#form_group_apply").submit(function(event) {
		event.preventDefault();
		var vals = $(this).serialize();
		$.post("/activity/join_group_apply/", vals, function(json) {
			$("#dlg_group_apply").dialog("close");
			if(json['success']) {
				$(".ui-layout-center").load('/activity/joined_groups/');
			}
		});
	});
};
// create_dlg_group_apply
var create_dlg_create_group = function() {
	$("#dlg_create_group").dialog({
		autoOpen : false,
		modal : true
	});

	$("#form_create_group").submit(function(event) {
		event.preventDefault();
		var vals = $(this).serialize();
		$.post("/activity/create_group/", vals, function(json) {
			$("#dlg_create_group").dialog("close");
			if(json['success']) {
				show_managed_groups();
			}
		});
	});
};
// create_dlg_create_group
var form_settle_activity = function() {
	if($("#form_settle").length == 0)
		return;
	$("#btn_add_settle").button();
	$("#btn_add_settle").click(function() {
		$tbody = $("#form_settle table tbody");
		tr = $("#form_settle table tbody tr")[0];
		new_tr = tr.cloneNode(true);
		id = $tbody.children().length;
		new_tr.children[0].children[0].name = "set_lst[" + id + "]['groupship']";
		new_tr.children[1].children[0].name = "set_lst[" + id + "]['balance_pay']";
		new_tr.children[1].children[0].value = "0";
		new_tr.children[2].children[0].name = "set_lst[" + id + "]['cash_pay']";
		new_tr.children[2].children[0].value = "0";
		new_tr.children[3].children[0].name = "set_lst[" + id + "]['remark']";
		new_tr.children[3].children[0].value = "";
		$tbody.append(new_tr);
	});
	$("#form_settle").submit(function(event) {
		event.preventDefault();
		
		var ret = true;
		var gs = Array();
		var message = "";
		var $settles = $("#form_settle table tbody tr");
		$.each($settles, function(n, val) {
			var gsid = val.children[0].children[0].value;
			gs.push(gsid);
			if ( gs.indexOf(gsid) != gs.lastIndexOf(gsid) ) {
				message = "同一个组员不能有两条结算信息！";
				ret = false;
			}
			if ( (val.children[1].children[0].value.length == 0) || 
				(val.children[2].children[0].value.length == 0) ) {
				message = "余额支付或者现金支付不能为空！";
				ret = false;
			}
		});
		
		if ( ret == false ) {
			alert(message);
			return false;
		}
		
		ret = confirm("提交后不能修改结算信息，确定要提交吗？")
		if ( ret == false ) {
			return false;
		}
				
		var vals = $(this).serialize();
		$.post("/activity/settle_activity/", vals, function(json) {
			if(json['success'])
				show_group_detail(json['gid']);
		});
		window.location.hash = "tabs-recent-activity";
	});
};
// form_settle_activity
var form_cancel_apply = function() {
	if($("#form_cancel_apply").length == 0)
		return;
	$("#form_cancel_apply").submit(function(event) {
		event.preventDefault();
		var vals = $(this).serialize();
		$.post("/activity/cancel_apply/", vals, function(data) {
			$("#dlg_apply").dialog("close");
			$(".ui-layout-center").html(data);
			decorate_group_detail();
		});
		window.location.hash = "tabs-recent-activity";
	});
};
// form_cancel_apply
var form_chg_pwd = function() {
	$("#form_chg_pwd").submit(function(event) {
		event.preventDefault();
		$("#form_chg_pwd #old_pwd, #password1, #password2").removeClass("ui-state-error");
		var $tips = $("#tabs-chg-pwd .validate-tips");
		var $password1 = $("#form_chg_pwd #password1");
		var $password2 = $("#form_chg_pwd #password2");

		if(!check_length($password1, 6, 8)) {
			update_tips($tips, "密码应为 6 ~ 8 个字符!");
			return;
		}
		if($password1.val() != $password2.val()) {
			update_tips($tips, "两次输入的密码不一致!");
			$password1.addClass("ui-state-error");
			$password2.addClass("ui-state-error");
			return;
		}
		var vals = $(this).serialize();
		$.post("/activity/chg_pwd/", vals, function(json) {
			if(json['success'] == true) {
				update_tips($tips, "密码修改成功!");
				$("#form_chg_pwd #old_pwd").val("");
				$password1.val("");
				$password2.val("");
			} else if(json['old_pwd_err']) {
				update_tips($tips, "旧密码错误!");
				$("#form_chg_pwd #old_pwd").addClass("ui-state-error");
			} else if(json['new_pwd_err']) {
				update_tips($tips, "两次输入的密码不一致!");
				$("#form_chg_pwd #password1").addClass("ui-state-error");
				$("#form_chg_pwd #password2").addClass("ui-state-error");
			}
		});
	});
};
// form_chg_pwd
var form_chg_personal_info = function() {
	$("#form_chg_personal_info").submit(function(event) {
		event.preventDefault();

		var $last_name = $("#form_chg_personal_info #last_name");
		var $first_name = $("#form_chg_personal_info #first_name");
		var $email = $("#form_chg_personal_info #email");
		var $tips = $("#tabs-personal-info .validate-tips");

		$last_name.removeClass("ui-state-error");
		$first_name.removeClass("ui-state-error");
		$email.removeClass("ui-state-error");

		if(!check_length($last_name, 1, 6)) {
			update_tips($tips, "请输入姓氏!(1 ~ 6  个字符)");
			return;
		}
		if(!check_length($first_name, 1, 6)) {
			update_tips($tips, "请输入名字!(1 ~ 6 个字符)");
			return;
		}
		if(!check_email($email)) {
			update_tips($tips, "请输入正确的 email 地址!");
			return;
		}

		var vals = $(this).serialize();
		$.post("/activity/chg_personal_info/", vals, function(json) {
			if(json['email_used'] == true) {
				update_tips($tips, "该电子邮件已经被使用!");
				email.addClass("ui-state-error");
			} else if(json['success'] == true) {
				update_tips($tips, "成功保存个人信息!");
			}
		});
	});
};
// form_chg_personal_info
var decorate_group_detail = function() {
	if($(".group-detail").length == 0)
		return;
	$("input:submit, .button").button();
	$(".group-detail").tabs();
	$("#tabs-activity-records > table, #tabs-group-members > table").ariaSorTable({
		rowsToShow : 10,
		pager : true
	});

	form_settle_activity();
	form_cancel_apply();
};
// decorate_group_detail
var show_group_detail = function(gid) {
	$(".ui-layout-center").load('/activity/group/?gid=' + gid, function() {
		decorate_group_detail();
	});
};
// show_group_detail
var show_activity_detail = function(aid) {
	$(".activity-detail").load('/activity/activity_detail/?id=' + aid);
};
// show_activity_detail
var show_group_act_detl = function(gid, aid) {
	$(".ui-layout-center").load('/activity/group/?gid=' + gid, function() {
		decorate_group_detail();
		show_activity_detail(aid);
	});
};
// show_group_act_detl
var show_sys_msgs = function() {
	$(".ui-layout-center").load('/activity/sys_msgs/', function() {
		$(".sys-msg").tabs();
		$("#form_group_apply").submit(function(event) {
			event.preventDefault();
			var vals = $(this).serialize();
			$.post("/activity/process_group_apply/", vals, function(json) {
				if(json['success'] != true) {
					console.debug(json['message'])
				}
				show_sys_msgs();
			});
		});
	});
};
// show_sys_msgs
var on_send_test_mail = function() {
	var $email = $("#form_chg_personal_info #email");
	var $tips = $("#tabs-personal-info .validate-tips");
	if(!check_email($email)) {
		update_tips($tips, "请输入正确的 email 地址!");
		return;
	}
	$.get("/activity/send_test_mail/", {
		'email' : $email.val()
	}, function(json) {
		if(json['success'] == true)
			update_tips($tips, "成功发送测试邮件, 请注意查收!");
	});
};
// on_send_test_mail
var show_personal_info = function() {
	$(".ui-layout-center").load('/activity/personal_infos/', function() {
		$(".personal-infos").tabs();
		$("input:submit, .button").button();
		form_chg_pwd();
		form_chg_personal_info();
	});
};
// show_personal_info
var show_account_detail = function() {
	$(".ui-layout-center").load('/activity/account_detail/', function() {
		$(".account-detail > table").ariaSorTable({
			rowsToShow : 15,
			pager : true
		});
	});
};
// show_account_detail
var show_activities = function() {
	$(".ui-layout-center").load('/activity/activities/', function() {
		$(".activities > table").ariaSorTable({
			rowsToShow : 10,
			pager : true
		});
	});
};
// show_activities
var show_managed_groups = function() {
	$(".ui-layout-center").load('/activity/managed_groups/', function() {
		$(".button").button();
	});
};
// show_managed_groups
var prepare_dlg = function(dlg_type) {
	var create_dict = {
		"dlg_recharge" : create_dlg_recharge,
		"dlg_add_activity" : create_dlg_add_activity,
		"dlg_chg_activity" : create_dlg_chg_activity,
		"dlg_apply" : create_dlg_apply,
		"dlg_group_apply" : create_dlg_group_apply,
		"dlg_create_group" : create_dlg_create_group
	}
	var query = "[aria-labelledby=ui-dialog-title-" + dlg_type + "]";
	if($(query).length != 0)
		return;

	$.ajax({
		url : "/activity/get_dlg/",
		data : {
			"dlg_type" : dlg_type
		},
		async : false,
		success : function(data) {
			$("#inner-body").append(data);
			$("input:submit").button();
			create_dict[dlg_type]();
		}
	});
}
// prepare_dlg
var on_recharge = function(groupship) {
	prepare_dlg("dlg_recharge");
	$("#form_recharge #groupship").val(groupship);
	$("#dlg_recharge").dialog("open");
};
// on_recharge
var on_add_activity = function(group) {
	prepare_dlg("dlg_add_activity");
	$("#form_add_activity #group").val(group);
	$("#dlg_add_activity").dialog("open");
};
// on_add_activity
var on_chg_activity = function(activity, date, total_fee, remark) {
	prepare_dlg("dlg_chg_activity");
	$("#form_chg_activity #activity").val(activity);
	$("#form_chg_activity #date").val(date);
	$("#form_chg_activity #total_fee").val(total_fee);
	$("#form_chg_activity #remark").val(remark);
	$("#dlg_chg_activity").dialog("open");
};
// on_chg_activity
var on_apply = function(activity) {
	prepare_dlg("dlg_apply");
	$("#form_apply #activity").val(activity);
	$("#dlg_apply").dialog("open");
};
// on_apply
var on_group_apply = function(group_name, group) {
	prepare_dlg("dlg_group_apply");
	$("#ui-dialog-title-dlg_group_apply").text("申请加入小组：" + group_name);
	$("#form_group_apply #group").val(group);
	$("#dlg_group_apply").dialog("open");
};
// on_group_apply
var on_group_apply_accepted = function(apply) {
	$("#form_group_apply #apply").val(apply);
	$("#form_group_apply #accepted").val(1);
	$("#form_group_apply").submit();
};
// on_group_apply_accepted
var on_group_apply_denied = function(apply) {
	$("#form_group_apply #apply").val(apply);
	$("#form_group_apply #accepted").val(0);
	$("#form_group_apply").submit();
};
// on_group_apply_denied
var on_create_group = function() {
	prepare_dlg("dlg_create_group");
	$("#dlg_create_group").dialog("open");
};
// on_create_group