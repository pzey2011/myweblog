from django.conf.urls import url
from .views import UserLoginView,UserPostCreateView,UserPostListView,UserRegisterView

urlpatterns = [
    url(r'^login/$', UserLoginView.as_view()),
    url(r'^index/$', UserPostListView.as_view()),
    url(r'^register/$', UserRegisterView.as_view())
]