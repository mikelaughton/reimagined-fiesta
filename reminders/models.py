from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from datetime import datetime
def _(arg):
	#Dummy _ function pending i18n, which you've forgotten.
	return arg

# Create your models here.

class Icon(models.Model):
	#Sysadmin only model, so no need to isolate by user.
	icon = models.ImageField(upload_to='uploads/%Y/%m/%d/')
	description = models.CharField(_('Description'),blank=True,null=True,max_length=100)
	def __str__(self):
		return self.description

#This should be a theme choice, i.e., naming a class, not designating a colour. Crazy lack of flexibility. Moron.
COLOUR_CHOICES = [('#F44336', 'red'), ('#4CAF50', 'green'), ('#FFEB3B', 'yellow'), ('#2196F3', 'blue')]

class Task(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,blank=True,null=True)
	label = models.CharField(max_length=200)
	entry_date = models.DateTimeField(_('Date entered'))
	deadline = models.DateTimeField(_('Deadline'),blank=True,null=True)
	icon = models.ForeignKey(Icon,null=True,blank=True)
	is_secret = models.BooleanField(_('Secret?'))
	#Mebs change the widget on this.
	countdown = models.BooleanField(_('Countdown'),help_text=_('Countdown or countup?'),default=True)
	colour = models.CharField(_('Colour'),choices=COLOUR_CHOICES,default=COLOUR_CHOICES[0][0],max_length=7)
	def last_performed(self):
		return self.performance_set.order_by('-perf_date')[0].perf_date
	def __str__(self):
		return self.label

class Performance(models.Model):
	#For when a task is performed.
	task = models.ForeignKey(Task)
	perf_date = models.DateTimeField(_('Date performed'))
	def __str__(self):
		return "{}: {}".format(self.task.pk,self.perf_date)
