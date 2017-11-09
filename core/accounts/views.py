from django.shortcuts import render
from math import ceil
from django.views.generic import ListView, CreateView, DetailView
from django.utils.translation import ugettext_lazy as _

from .models import Profile
from .forms import LoginForm,RegisterForm
from core.posts.models import Post, Tag, Comment

class UserRegisterView(CreateView):
    model = Profile
    template_name = 'accounts/register.html'
    form_class = RegisterForm

    def get(self, request, *args, **kwargs):

        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):

        form = self.form_class(request.POST)
        if form.is_valid():
            # todo erase print
            print('form.user_data: ', form.cleaned_data)

            user = form.save(form.cleaned_data)
        else:
            return render(request, self.template_name, {'form': form})

        return UserPostListView.as_view()(self,user)

class UserLoginView(CreateView):
    model = Profile
    template_name = 'accounts/login.html'
    form_class = LoginForm

    def get(self, request, *args, **kwargs):

        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):

        form = self.form_class(request.POST)
        # todo erase print
        print(form)
        if form.is_valid():

            user = form.login(form.cleaned_data)
        else:
            return render(request, self.template_name, {'form': form})

        return UserPostListView.as_view()(self,user)


# json_response=json.loads(response.text)
# class UserPostCreateView(CreateView):
#    model = Post

class UserPostListView(ListView):
    model = Post
    template_name = 'accounts/account_index.html'

    def get_queryset(self,user):
        queryset = Post.objects.filter(author=user)

    def get_context_data(self,user, **kwargs):
        context = super(UserPostListView, self).get_context_data(**kwargs)
        context['tag_list'] = Tag.objects.filter(posts__author=self.request.user)
        context['half_tag_count'] = ceil(Tag.objects.all().count() / 2)
        return context

class UserPostCreateView(CreateView):
    model = Post
    template_name = 'accounts/create_post.html'
'''
    def get_queryset(self):
        queryset = Post.objects.filter(author=self.request.user)

    def get_context_data(self, **kwargs):
        context = super(UserPostListView, self).get_context_data(**kwargs)
        context['tag_list'] = Tag.objects.all()
        context['half_tag_count'] = ceil(Tag.objects.all().count() / 2)
        return context
'''