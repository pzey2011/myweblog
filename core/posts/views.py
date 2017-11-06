from django.shortcuts import render
from math import ceil
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from .serializers import PostCreateSerializer, PostItemSerializer,TagCreateSerializer,TagSerializer
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.views.generic import ListView,CreateView,DetailView
from .models import Post,Tag,Comment
from .response import ApiResponse

def get_tag_posts(kwargs):
    posts = []
    for post in Post.objects.all():
        if post.tags.filter(name__exact=kwargs['object']).exists():
            posts.append(post)

    return posts
# Create your views here.
class ApiPostCreateView(generics.CreateAPIView):

    serializer_class = PostCreateSerializer
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if self.set_user:
            serializer.user = request.user

        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(ApiResponse.get_base_response(response_code=status.HTTP_201_CREATED,
                                                      data={self.model_name: serializer.data},
                                                      message=self.message['create']),
                        status=status.HTTP_201_CREATED, headers=headers)

class PostListView(ListView):
    model = Post
    template_name = 'posts/index.html'

    def get_context_data(self, **kwargs):
        context = super(PostListView, self).get_context_data(**kwargs)
        context['tag_list'] = Tag.objects.all()
        context['half_tag_count'] = ceil(Tag.objects.all().count()/2)
        return context

class PostDetailView(DetailView):
    model = Post
    template_name = 'posts/detail.html'

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        context['post_list'] = get_tag_posts(kwargs)
        context['tag_list'] = Tag.objects.all()
        context['half_tag_count'] = ceil(Tag.objects.all().count()/2)
        return context

class TagPostListView(DetailView):
    model = Tag
    template_name = 'posts/index.html'

    def get_context_data(self, **kwargs):
        context = super(TagPostListView, self).get_context_data(**kwargs)
        context['post_list']=get_tag_posts(kwargs)
        context['tag_list'] = Tag.objects.all()
        context['half_tag_count'] = ceil(Tag.objects.all().count()/2)
        return context
