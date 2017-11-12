from django.shortcuts import render,redirect
from math import ceil
from django.views.generic import ListView, CreateView, DetailView
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import login
from rest_framework.permissions import IsAuthenticated


from .models import Profile,get_group
from .forms import LoginForm,RegisterForm,PostCreateForm
from core.posts.models import Post, Tag, Comment

class UserRegisterView(CreateView):
    model = Profile
    template_name = 'accounts/register.html'
    form_class = RegisterForm

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return redirect('index')
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):

        form = self.form_class(request.POST)
        if form.is_valid():
            user=form.save(form.cleaned_data)
            login(request,user)
            return redirect('index')
        else:
            return render(request, self.template_name, {'form': form})



class UserLoginView(ListView):
    model = Profile
    template_name = 'accounts/login.html'
    form_class = LoginForm

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return redirect('index')
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):

        form = self.form_class(request.POST)
        if form.is_valid():
            login(request, form.cleaned_data.get('user'))
            return redirect('index')
        else:
            return render(request, self.template_name, {'form': form})




# json_response=json.loads(response.text)
# class UserPostCreateView(CreateView):
#    model = Post

class UserPostListView(ListView):
    model = Post
    template_name = 'accounts/account_index.html'
    form_class = PostCreateForm
    permission_class=[IsAuthenticated,]

    def get_queryset(self):
        queryset = Post.objects.filter(author=self.request.user)

    def get_context_data(self, **kwargs):
        context = super(UserPostListView, self).get_context_data(**kwargs)

        profile = Profile.objects.get(id=self.request.user.id)
        #todo erase print
        print("url: ",profile.avatar.url)
        context['avatar_url'] = profile.avatar.url
        context['tag_list'] = Tag.objects.filter(posts__author=self.request.user)
        context['half_tag_count'] = ceil(Tag.objects.all().count() / 2)
        return context
    def get(self, request, *args, **kwargs):
        form = self.form_class()

        return render(request, self.template_name, {'form': form})

class UserPostCreateView(CreateView):
    model = Post
    template_name = 'accounts/index.html'
    permission_class = [IsAuthenticated, ]
'''
    def get_queryset(self):
        queryset = Post.objects.filter(author=self.request.user)

    def get_context_data(self, **kwargs):
        context = super(UserPostListView, self).get_context_data(**kwargs)
        context['tag_list'] = Tag.objects.all()
        context['half_tag_count'] = ceil(Tag.objects.all().count() / 2)
        return context
'''