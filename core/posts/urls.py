from django.conf.urls import url
from core.posts.views import PostListView,ApiPostCreateView,PostDetailView

urlpatterns = [
    url(r'^api/posts/$', ApiPostCreateView.as_view()),
    url(r'^$', PostListView.as_view()),
    url(r'^post/(?P<pk>\d+)$', PostDetailView.as_view(), name='book-detail')
   # url(r'^posts/list/$', PostListView.as_view()),
   # url(r'^posts/comment/$', CommentCreateView.as_view()),
   # url(r'^posts/(?P<pk>[0-9]+)/$', PostItemView.as_view()),
  #  url(r'^tags/$', TagCreateView.as_view())

]