from math import ceil
from django.contrib.auth.models import User
from django.views.generic import ListView,CreateView,DetailView
from django.http import HttpResponse
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

        context['post_list']=admin_posts
        context['user']=self.request.user
        admin_tags=[]
        for post in admin_posts:
            admin_tags.extend(list (post.tags.all()))
        # todo erase print
        print('admin_tags: ', admin_tags)

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
        # todo erase print
        print('tags: ', admin_tags)

        context['tag_list'] = admin_tags
        context['half_tag_count'] = ceil(len(admin_tags)/2)
        return context

    def get(self, request, *args, **kwargs):
        super(PostDetailView, self).get(self, request, *args, **kwargs)
        admin = User.objects.filter(is_superuser=True)
        # todo erase post
        print('post : ',self.post )

        if self.post not in Post.objects.filter(author=admin):
            return HttpResponse('You don\'t have permission to access this post', status=403)


class TagPostListView(DetailView):
    model = Tag
    template_name = 'posts/index.html'

    def get_context_data(self, **kwargs):
        context = super(TagPostListView, self).get_context_data(**kwargs)
        context['user'] = self.request.user
        self.tag_posts=get_tag_posts(kwargs)
        context['post_list']=self.tag_posts
        context['tag_list'] = Tag.objects.all()
        context['half_tag_count'] = ceil(Tag.objects.all().count()/2)
        return context
    def get(self, request, *args, **kwargs):
        super(TagPostListView, self).get(self, request, *args, **kwargs)
        if len(self.tag_posts)== 0:
            return HttpResponse('You don\'t have permission to access the posts of this tag', status=403)


