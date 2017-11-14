from django.views.generic.edit import UpdateView
from django.shortcuts import render,redirect,render_to_response
from django.http import HttpResponseRedirect
from math import ceil
from django.views.generic import ListView, CreateView, DetailView
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.template import RequestContext
from django.contrib.auth import login
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Profile,get_group
from .forms import LoginForm,RegisterForm,PostCreateForm,UserProfileUpdateForm,CommentCreateForm
from core.posts.models import Post, Tag, Comment

def find_tags(text):
    tags_positions = [i for i, letter in enumerate(text) if letter == '#']
    tags = []

    for tag_position in tags_positions:
        tag = ''
        istag = False
        for i, c in enumerate(text):
            if i == tag_position:
                istag = True
            elif istag and (text[i] != ' '):
                tag += text[i]
            elif (text[i] == ' ') and istag:
                istag = False
                tags.append(tag)
                break
            if i == (len(text) - 1) and istag:
                tags.append(tag)

    tags = list(set(tags))
    return tags
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


class UserProfileUpdateView(UpdateView):
    form_class = UserProfileUpdateForm
    model = Profile
    template_name_suffix = '_update'
    success_url = '/accounts/index/'

    def get_object(self):
        return Profile.objects.get(id=self.request.user.id)

    def form_valid(self, form):
        # save cleaned post data
        clean = form.cleaned_data
        form.save(clean)
        return HttpResponseRedirect('/accounts/index/')


class UserPostListView(ListView):
    model = Post
    template_name = 'accounts/account_index.html'

    def get_context_data(self, **kwargs):
        context = super(UserPostListView, self).get_context_data(**kwargs)

        profile = Profile.objects.get(id=self.request.user.id)
        context['avatar_url'] = profile.avatar.url
        posts=Post.objects.filter(author=self.request.user)
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
        context['post_list']=posts
        context['tag_list'] = Tag.objects.filter(posts__author=self.request.user).distinct()
        context['half_tag_count'] = ceil(context['tag_list'].count() / 2)
        self.context=context
        return context

    @method_decorator(login_required, name='dispatch')
    def get(self, request, *args, **kwargs):
        super(UserPostListView, self).get(self, request, *args, **kwargs)
        profile = Profile.objects.get(id=self.request.user.id)
        post_create_form = PostCreateForm()
        comment_create_form = CommentCreateForm()
        self.context['post_create_form']=post_create_form
        self.context['comment_create_form']=comment_create_form
        # todo erase print
        print("context: ",self.context )
        return render(request, 'accounts/account_index.html',self.context)

    @method_decorator(login_required, name='dispatch')
    def post(self, request):#post creation
        post_create_form = PostCreateForm(request.POST, request.FILES)
        comment_create_form = CommentCreateForm(request.POST)
        print('(post) comment create form: ',comment_create_form)
        if post_create_form.is_valid():
            print('post create')
            self.text = post_create_form.cleaned_data.get('text')
            new_post=post_create_form.cleaned_data
            new_post['author']=User.objects.get(id=self.request.user.id)

            post = Post.objects.create(**new_post)

            tags=find_tags(self.text)
            post.tags=[]
            for tag in tags:
                tag_object=Tag.objects.get_or_create(name=tag)[0]
                post.tags.add(tag_object)
            post.save()

        elif comment_create_form.is_valid():
            #todo erase print
            print('comment create cleaned data:',comment_create_form.cleaned_data)
            post_id = comment_create_form.cleaned_data.get('post_id')
            # todo erase print
            print('post_id: ',post_id)

            new_comment = comment_create_form.cleaned_data
            # todo erase print
            print('create comment form data: ', comment_create_form.cleaned_data)

            new_comment['author'] = User.objects.get(id=self.request.user.id)

            comment = Comment.objects.create(**new_comment)
            # todo erase print
            print('comment: ', comment)

            comment.post=Post.objects.get(id=post_id)
            # todo erase print
            print('post of comment',comment.post)
            comment.save()
        return redirect('index')


class UserTagPostListView(DetailView):
    model = Tag
    template_name = 'accounts/account_tag_posts.html'

    def get_context_data(self, **kwargs):
        context = super(UserTagPostListView, self).get_context_data(**kwargs)

        profile = Profile.objects.get(id=self.request.user.id)
        context['avatar_url'] = profile.avatar.url
        posts = []
        user_posts = Post.objects.filter(author=self.request.user)
        for post in user_posts:
            if post.tags.filter(name__exact=kwargs['object']).exists():
                posts.append(post)

        context['post_list']=posts
        context['tag_list'] = Tag.objects.filter(posts__author=self.request.user).distinct()
        context['half_tag_count'] = ceil(context['tag_list'].count() / 2)
        self.context=context
        return context

    @method_decorator(login_required, name='dispatch')
    def get(self, request, *args, **kwargs):
        super(UserTagPostListView, self).get(self, request, *args, **kwargs)
        return self.render_to_response(self.context)