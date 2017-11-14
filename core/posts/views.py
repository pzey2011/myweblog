from django.shortcuts import render
from math import ceil
from django.contrib.auth.models import User
from django.views.generic import ListView,CreateView,DetailView
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Post,Tag,Comment


def get_tag_posts(kwargs):
    posts = []
    admin = User.objects.filter(is_superuser=True)
    admin_posts = Post.objects.filter(author=admin)
    for post in admin_posts:
        if post.tags.filter(name__exact=kwargs['object']).exists():
            posts.append(post)

    return posts

class PostListView(ListView):
    model = Post
    template_name = 'posts/index.html'

    def get_context_data(self, **kwargs):
        context = super(PostListView, self).get_context_data(**kwargs)
        admin = User.objects.filter(is_superuser=True)
        admin_posts = Post.objects.filter(author=admin)

        paginator = Paginator(admin_posts, 4)
        page = self.request.GET.get('page')
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            posts = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            admin_posts = paginator.page(paginator.num_pages)
        context['num_of_pages'] = range(1, paginator.num_pages + 1)

        context['post_list']=admin_posts
        context['user']=self.request.user
        admin_tags=[]
        for post in admin_posts:
            admin_tags.extend(list (post.tags.all()))
        admin_tags=list(set(admin_tags))#remove duplicate tags from sidebar

        context['tag_list']=admin_tags
        context['half_tag_count'] = ceil(len(admin_tags)/2)
        return context

class PostDetailView(DetailView):
    model = Post
    template_name = 'posts/detail.html'

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        context['user'] = self.request.user
        self.post=context['post']
        admin = User.objects.filter(is_superuser=True)
        admin_posts = Post.objects.filter(author=admin)

        admin_tags = []
        for post in admin_posts:
            admin_tags.extend(list(post.tags.all()))

        admin_tags = list(set(admin_tags))#remove duplicate tags from sidebar

        context['tag_list'] = admin_tags
        context['half_tag_count'] = ceil(len(admin_tags)/2)
        return context

    def get(self, request, *args, **kwargs):
        super(PostDetailView, self).get(self, request, *args, **kwargs)
        admin = User.objects.filter(is_superuser=True)

        if self.post not in Post.objects.filter(author=admin):
            return HttpResponse('You don\'t have permission to access this post', status=403)

        return render(request, self.template_name, self.get_context_data())

class TagPostListView(DetailView):
    model = Tag
    template_name = 'posts/index.html'

    def get(self, request, *args, **kwargs):
        super(TagPostListView, self).get(self, request, *args, **kwargs)

        if len(self.tag_posts)== 0:
            return HttpResponse('You don\'t have permission to access the posts of this tag', status=403)

        return render(request, self.template_name ,self.context)

    def get_context_data(self, **kwargs):
        context = super(TagPostListView, self).get_context_data(**kwargs)
        context['user'] = self.request.user
        posts = []
        admin = User.objects.filter(is_superuser=True)
        admin_posts = Post.objects.filter(author=admin)
        for post in admin_posts:
            if post.tags.filter(name__exact=kwargs['object']).exists():
                posts.append(post)

        self.tag_posts = posts
        paginator = Paginator(posts, 4)
        page = self.request.GET.get('page')
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            posts = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            posts = paginator.page(paginator.num_pages)

        context['num_of_pages'] = range(1, paginator.num_pages + 1)

        context['post_list']=posts

        tags = []
        for post in self.tag_posts:
            tags.extend(list(post.tags.all()))

        tags = list(set(tags))  # remove duplicate tags from sidebar

        context['tag_list'] = tags
        context['half_tag_count'] = ceil(len(tags) / 2)
        self.context=context
        return context


