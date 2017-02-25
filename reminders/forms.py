from django import forms
#from django.forms.extras.widget import SelectDateWidget
from reminders.models import *

class TaskForm(forms.ModelForm):
	class Meta:
		model = Task
		exclude = ['user']
		#widgets = { 'deadline':SelectDateWidget, 'entry_date': SelectDateWidget }
