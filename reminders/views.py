from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
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

	def get_queryset(self):
		return Task.objects.filter(user=self.request.user)

class RegisterView(generic.edit.CreateView):
	template_name = 'reminders/register.html'
	form_class = UserCreationForm
	success_url = '/'

class TaskDetailView(generic.DetailView):
	model = Task

@method_decorator(login_required, name='dispatch')
class TaskCreateView(generic.edit.CreateView):
	model = Task
	template_name_suffix = '_create'
	success_url = '/'
	form_class = TaskForm

	def form_valid(self,form):
		form.instance.user = self.request.user
		return super(TaskCreateView,self).form_valid(form)

class PerformanceChangeView(generic.edit.CreateView):
	model = Performance
	fields = ['perf_date']
	template_name_suffix = '_update_form'
	def get_context_data(self,**kwargs):
		context = super(PerformanceChangeView,self).get_context_data(**kwargs)
		return context

def PerformView(request,task_id):
	if request.method == "POST":
		the_task = get_object_or_404(Task,pk=task_id)
		new_perf = Performance(perf_date=datetime.now(),task=the_task)
		try:
			new_perf.save()
			return HttpResponse("Hurray")
		except KeyError:
			return HttpResponse("Key error.")
		else:
			return HttpResponse("Fail")
	elif request.method=="GET":
		#Set up a proper view.
		return HttpResponse("Nah mate.")
