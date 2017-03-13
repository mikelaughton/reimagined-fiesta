from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse, HttpResponseForbidden
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.contrib.auth import authenticate, login
#For @login_required
from django.contrib.auth.decorators import login_required
#For UserCreationForm
from django.contrib.auth.forms import UserCreationForm
#Because you can't decorate classes...
from django.utils.decorators import method_decorator
# Create your views here.

from .models import *
from reminders.forms import *

#Reverse lazy to stop there being a circular import error.
@method_decorator(login_required, name='dispatch')
class IndexView(generic.ListView):
	template_name = 'reminders/index.html'
	context_object_name = 'tasks'
	next = reverse_lazy("adulting:index")

	def get_queryset(self):
		return Task.objects.filter(user=self.request.user)

@method_decorator(login_required,name='dispatch')
class MasonryView(generic.ListView):
	template_name = 'reminders/index_masonry.html'
	context_object_name = 'tasks'
	next = reverse_lazy("adulting:index")
	form_media = TaskForm()
	form_media = str(form_media.media)
	def get_context_data(self,**kwargs):
		#Ask yourself the question, is this necessary?
		#Add in the form media for the datepicker widget
		#The 'create reminder' button depends on the media you supply to the form - if you change the form, you want the button to still work, because it's a pain in the arse.
		context = super(MasonryView,self).get_context_data(**kwargs)
		context['form']=str(self.form_media)
		return context
	def get_queryset(self):
		return Task.objects.filter(user=self.request.user).order_by('-entry_date')

class RegisterView(generic.edit.CreateView):
	template_name = 'reminders/register.html'
	form_class = UserCreationForm
	success_url = '/'

class TaskDetailView(generic.DetailView):
	model = Task

@method_decorator(login_required,name='dispatch')
class TaskDeleteView(generic.edit.DeleteView):
	#def ajax to send Json instead
	model = Task
	success_url = reverse_lazy("reminders:index")

#Ajax response mixin.
class AJAXMixin(object):
	def form_invalid(self,form):
		response = super(AJAXMixin,self).form_invalid(form)
		if self.request.is_ajax:
			return JsonResponse(form.errors,status=400)
		else:
			return response
			
	def form_valid(self,form):
		#Redirects to success_url normally
		response = super(AJAXMixin,self).form_valid(form)
		if self.request.is_ajax():
			#Let the view object query the object's PK.
			data = { 'pk': self.object.pk, }
			return JsonResponse(data)
		else:
			#Defined elsewhere
			return response

@method_decorator(login_required, name='dispatch')
class TaskCreateView(AJAXMixin,generic.edit.CreateView):
	model = Task
	template_name_suffix = '_create'
	success_url = '/'
	form_class = TaskForm

	def form_valid(self,form):
		form.instance.user = self.request.user
		return super(TaskCreateView,self).form_valid(form)

@login_required
def TaskCreateAjaxView(request):
	if request.is_ajax():
		form = TaskForm()
		#Pass the form to the JSON so it can be dynamically rendered.
		data = { 'status':'200', 'form':form.as_p() }
		return JsonResponse(data)
	else:
		return HttpResponseForbidden("Maybe you meant to go to <a href='{0}'>{0}</a>?".format(reverse_lazy("reminders:create")))

class PerformanceCreateView(generic.edit.CreateView):
	model = Performance
	fields = ['perf_date']
	template_name_suffix = '_update_form'
	
	def get_context_data(self,**kwargs):
		context = super(PerformanceChangeView,self).get_context_data(**kwargs)
		return context

def PerformView(request,task_id):
	the_task = get_object_or_404(Task,pk=task_id)
	if request.method == "POST":
		new_perf = Performance(perf_date=datetime.now(),task=the_task)
		if request.is_ajax:
			data = {}
			try:
				new_perf.save()
				data["message"]="Success"
				data["is_countdown"] = the_task.countdown
				return JsonResponse(data)
			except Exception:
				data["message"]="Failure"
				return JsonResponse(data)
		else:
			return HTTPResponseRedirect(reverse("adulting:index"))
	if request.method == "GET":
		form = PerformanceForm
		extra_context = {}
		extra_context['form'] = form
		return render(request,"reminders/performance_update_form.html",extra_context)
