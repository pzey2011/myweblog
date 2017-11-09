from django.shortcuts import render
from math import ceil
from django.views.generic import ListView,CreateView,DetailView
from django.utils.translation import ugettext_lazy as _

from .models import Account
from .forms import LoginForm
from core.posts.models import Post,Tag,Comment


class UserLoginView(CreateView):
    model = Account
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
            user = form.login(request)
        else:
            return render(request, self.template_name, {'form': form})

        return UserPostListView.as_view()(self.request)

# json_response=json.loads(response.text)
#class UserPostCreateView(CreateView):
#    model = Post

class UserPostListView(ListView):
    model = Post
    template_name = 'accounts/account_index.html'

    def get_queryset(self):
        queryset = Post.objects.filter(author=self.request.user)

    def get_context_data(self, **kwargs):
        context = super(UserPostListView, self).get_context_data(**kwargs)
        context['tag_list'] = Tag.objects.all()
        context['half_tag_count'] = ceil(Tag.objects.all().count() / 2)
        return context
