from django import forms
from bootstrap3_datetime.widgets import DateTimePicker
from reminders.models import *

my_attrs = {
	"inline":True,
	"sideBySide":True,
	"todayBtn":"linked",
	"bootstrap_version":3,
	"usel10n":True,
}

class TaskForm(forms.ModelForm):
	class Meta:
		model = Task
		exclude = ['user']
		widgets = { 'deadline': DateTimePicker(options=my_attrs), 'entry_date': DateTimePicker(options=my_attrs) }
		
class PerformanceForm(forms.ModelForm):
	class Meta:
		model = Performance
		exclude = ('task',)
		widgets = { 'perf_date': DateTimePicker(options=my_attrs) }
