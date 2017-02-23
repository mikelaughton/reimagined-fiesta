from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
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

#Reverse lazy to stop there being a circular import error.
@method_decorator(login_required, name='dispatch')
class IndexView(generic.ListView):
	template_name = 'reminders/index.html'
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
	
