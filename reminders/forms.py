from django import forms
from datetimewidget.widgets import DateTimeWidget
from reminders.models import *

attrs = {}

class TaskForm(forms.ModelForm):
	class Meta:
		model = Task
		exclude = ['user']
		widgets = { 'deadline': DateTimeWidget(usel10n=True, bootstrap_version=3), 'entry_date': DateTimeWidget(usel10n= True, bootstrap_version=3) }
