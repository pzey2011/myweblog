from django.conf.urls import url
from .views import UserLoginView,UserPostCreateView,UserPostListView,UserRegisterView
from django.contrib.auth.views import logout
from django.contrib.auth.views import login

urlpatterns = [
    url(r'^login/$', UserLoginView.as_view()),
    url(r'^index/$', UserPostListView.as_view(),name='index'),
    url(r'^register/$', UserRegisterView.as_view()),
    url(r'^logout/$',  logout, {'next_page': '/'}, name='logout')
]