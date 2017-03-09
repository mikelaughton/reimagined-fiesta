function getCookie(name) {
	//Pull a cookie. Thanks Django docs!
	var cookieValue = null;
	if (document.cookie && document.cookie !== '') {
		var cookies = document.cookie.split(';');
		for (var i = 0; i < cookies.length; i++) {
			var cookie = jQuery.trim(cookies[i]);
			// Does this cookie string begin with the name we want?
			if (cookie.substring(0, name.length + 1) === (name + '=')) {
			    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
			    break;
			}
		}
	}
	return cookieValue;
}
var csrftoken = getCookie('csrftoken');

var resettimer = function(obj){
	//Find the nearest time element and reset it to zero. 
	div = $( obj ).closest("div.activity-group");
	console.log( div );
	time_el = div.children("time").first();
	time_el.text("0 {% trans 'seconds' noop %}");
 };
	dismiss_task = function(obj){ return false; }
	change_timer = function(obj,new_text){ 
	timer = $(obj).parents(".activity-group").find("time").first();
	console.log(timer);
	timer.text(new_text);
}
perform_task = function(e){
	//Send AJAX request to relevant URL.
	url = e.target.href;
	task_no = e.target.href.split("perform/")[1];
	console.log("Task no:" + task_no);
	data =  {the_task:task_no, 
		csrfmiddlewaretoken: csrftoken };
	t = $.post(url,data);
		return t;
		}
perform_task_handler = function(req,e){
	//e is the event, req is the ajax obj.
	JSON = req.responseJSON;
	rtext = req.responseJSON.message;
	riscd = req.responseJSON.is_countdown;
	new_text = "0 seconds";
	if(!riscd & rtext=="Success"){ change_timer(e.target,new_text); $(e.target).addClass("btn-success");$(e.target).removeClass("btn-default"); }
	if(!riscd & rtext!="Success"){ $(e.target).addClass("btn-warning");$(e.target).removeClass("btn-default"); console.log("AJAX says: " + rtext); }
	if(riscd) { dismiss_task(e.target); }
}

disable_buttons = function(){
	//Tee up the buttons.	
	$("a.perform_action").click(function(e){
		e.preventDefault();
		$(e.target).removeClass("btn-success");
		$(e.target).addClass("btn-default");
		p = perform_task(e);
		p.done(function(){perform_task_handler(p,e);});
		});
		
}

init_done_buttons = function(){
	disable_buttons();
}

init_create_buttons = function() { return true; }
