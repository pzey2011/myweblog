
from django.shortcuts import render,redirect
from math import ceil
from django.views.generic import ListView, CreateView, DetailView
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from django.contrib.auth import login



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


    def get_context_data(self, **kwargs):
        context = super(UserPostListView, self).get_context_data(**kwargs)

        profile = Profile.objects.get(id=self.request.user.id)
        #todo erase print
        print("url: ",profile.avatar.url)
        context['avatar_url'] = profile.avatar.url
        context['post_list']=Post.objects.filter(author=self.request.user)
        context['tag_list'] = Tag.objects.filter(posts__author=self.request.user)
        context['half_tag_count'] = ceil(Tag.objects.all().count() / 2)
        return context

    @method_decorator(login_required, name='dispatch')
    def get(self, request, *args, **kwargs):
        super(UserPostListView, self).get(self, request, *args, **kwargs)
        profile = Profile.objects.get(id=self.request.user.id)
        #todo erase print
        print("url1: ", profile.avatar.url)
        form = self.form_class()
       # print('form_html: ', form.as_ul())
        return self.render_to_response(self.get_context_data(form=form))

    @method_decorator(login_required, name='dispatch')
    def post(self, request):

        form = self.form_class(request.POST)
        print('form_data: ',form.data)
        if form.is_valid():

            self.text = form.cleaned_data.get('text')

            tags_pos = [i for i, letter in enumerate(self.text) if letter == '#']
            tags=[]

            for tag_pos in tags_pos:
                tag=''
                istag=False
                for i,c in enumerate(self.text):
                    if i==tag_pos:
                        istag=True
                    elif istag and (self.text[i]!=' '):
                        tag += self.text[i]
                        print('tag',tag)
                    elif (self.text[i]==' ') and istag:
                        istag=False
                        tags.append(tag)
                        break
                    if i==(len(self.text)-1) and istag:
                        tags.append(tag)

            tags = list(set(tags))

            # get or create tags  re.search('(?<=^#)\w+',self.text)
            # add tags to cleaned data for post creation
            new_post=form.cleaned_data
            new_post['author']=User.objects.get(id=self.request.user.id)
            new_post['tags']=[]
            new_post.pop('tags')
            # todo erase print
            print('newpost_data: ',new_post)

            post = Post.objects.create(**new_post)
            for tag in tags:
                post.tags.get_or_create(name=tag)
            # todo erase print
            print('post: ', post)
            post.save()

        return redirect('index')

