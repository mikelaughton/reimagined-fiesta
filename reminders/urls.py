from django.conf.urls import url
from . import views

app_name = "reminders"
urlpatterns = [
	url(r'^$',views.MasonryView.as_view(),name='index'),
	#url(r'^masonry$',views.MasonryView.as_view(),name='masonry'),
	url(r'^register/?$', views.RegisterView.as_view(),name='register'),
	url(r'^detail/(?P<pk>[0-9]*)/?$', views.TaskDetailView.as_view(),name='detail'),
	url(r'^perform/(?P<task_id>[0-9]*)/?$', views.PerformView, name='perform'),
	url(r'^create/?',views.TaskCreateView.as_view(),name='create'),
	url(r'^delete/(?P<pk>[0-9]*)/?',views.TaskDeleteView.as_view(),name='delete'),
]
