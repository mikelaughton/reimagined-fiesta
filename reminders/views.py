from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic

# Create your views here.

from .models import *

class IndexView(generic.ListView):
	template_name = 'reminders/index.html'
	context_object_name = 'tasks'

	def get_queryset(self):
		return Task.objects.filter(user=self.request.user)
