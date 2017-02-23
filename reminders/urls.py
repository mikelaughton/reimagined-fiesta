from django.conf.urls import url
from . import views

app_name = "reminders"
urlpatterns = [
	url(r'^$',views.IndexView.as_view(),name='index'),
	url(r'^register/?$', views.RegisterView.as_view(),name='register'),
	url(r'^detail/(?P<pk>[0-9]*)/?$', views.TaskDetailView.as_view(),name='detail'),
]
