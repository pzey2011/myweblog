from django.conf.urls import url
from .views import UserLoginView,UserPostListView,UserRegisterView,UserTagPostListView,UserProfileUpdateView
from django.contrib.auth.views import logout
from django.contrib.auth.views import login

urlpatterns = [
    url(r'^login/$', UserLoginView.as_view(),name='login'),
    url(r'^index/$', UserPostListView.as_view(),name='index'),
    url(r'^register/$', UserRegisterView.as_view(),name='register'),
    url(r'^logout/$',  logout, {'next_page': '/'}, name='logout'),
    url(r'^tags/(?P<pk>\d+)/posts/$', UserTagPostListView.as_view(), name='tag-posts'),
    url(r'^update/$', UserProfileUpdateView.as_view(),name='update-profile')
]