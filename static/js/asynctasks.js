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

//You could make this work too.
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

//You could make this more generic but let's run with it for now.
disable_buttons = function(){
	//Tee up the buttons.  Class should really be called perform_task.	
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
var task_create_clone = $('<div class="activity-group well task-create">' + "<h1>Create reminder</h1>" +
'<p id="create_button" style="font-size:400%;"><a href="/create" class="create_task">+</a></p>' +'</div>');
restore_task_create = function(){
	console.log(task_create_clone);
	$(".task-create").replaceWith(task_create_clone);
	$grid.masonry('layout');
}

build_create_form = function(obj,get_url,post_url){
	form_req = $.getJSON(get_url,function(resp){
		form = $( "<form/>",{action:post_url,method:"POST"});
		h1 = $("<h1>Create</h1>");
		$(form).append(h1);
		$(form).append($(resp.form));
		$(form).append($('<input type="submit" value="Submit" class="btn btn-success"> <a class="btn btn-warning" id="cancel_create_button">Cancel</a>'));
		$grid.on('click','#cancel_create_button',restore_task_create);
		$(form).append('<input type="hidden" value="'+csrftoken+'" name="csrfmiddlewaretoken">');
		$(obj).append(form);
		//I do not know why this works, but it does.
		$grid.masonry();
		});
}

init_create_buttons = function(action_url) { 
	$("a.create_task").click(function(e){
		console.log("Clicked.");
		e.preventDefault();
		div = $("<div/>",{'class':'grid-item','id':'newForm'});
		form_container = $("<div/>",{'class':'well activity-group task-create',});
		$(div).append(form_container)
		form = build_create_form(form_container,action_url,e.target.href);
		$div = $(div);
		$(".task-create").first().replaceWith(form_container);
		//$("#create_button").hide();
		$grid.masonry('layout');
	});
 }
