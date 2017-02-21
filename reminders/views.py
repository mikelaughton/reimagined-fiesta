from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.contrib.auth import authenticate, login
#For @login_required
from django.contrib.auth.decorators import login_required
#Because you can't decorate classes...
from django.utils.decorators import method_decorator
# Create your views here.

from .models import *

@method_decorator(login_required,name='dispatch')
class IndexView(generic.ListView):
	template_name = 'reminders/index.html'
	context_object_name = 'tasks'

	def get_queryset(self):
		return Task.objects.filter(user=self.request.user)
