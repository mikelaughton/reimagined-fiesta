from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

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

class Task(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,blank=True,null=True)
	label = models.CharField(max_length=200)
	entry_date = models.DateTimeField(_('Date entered'))
	deadline = models.DateTimeField(_('Deadline'),blank=True,null=True)
	icon = models.ForeignKey(Icon,null=True,blank=True)
	is_secret = models.BooleanField(_('Secret?'))

	def last_performed(self):
		return self.performance_set.perf_date().order_by('-perf_date')[0]
	def __str__(self):
		return self.label

class Performance(models.Model):
	#For when a task is performed.
	task = models.ForeignKey(Task)
	perf_date = models.DateTimeField(_('Date performed'))