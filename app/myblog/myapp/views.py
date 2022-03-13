from django.utils import timezone
from django.shortcuts import redirect, render, resolve_url
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import TemplateView, CreateView, DetailView, UpdateView, DeleteView, ListView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from .models import Post, Like
from .forms import PostForm, LoginForm, SignUpForm


class OnlyMyPostMixin(UserPassesTestMixin):
    raise_exception = True
    def test_func(self):
        post = Post.objects.get(id = self.kwargs['pk'])
        return post.author == self.request.user


class Index(TemplateView):
    template_name = 'myapp/index.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        post_list = Post.objects.all().order_by('-created_at')
        context = {
            'post_list': post_list,
        }
        return context
    
    
class PostCreate(OnlyMyPostMixin, CreateView):
    model = Post
    form_class = PostForm
    success_url = reverse_lazy('myapp:index')
    template_name = 'myapp/post_form.html'
    
    def form_valid(self, form):
        form.instance.author_id = self.request.user.id
        return super(PostCreate, self).form_valid(form)
    
    def get_success_url(self):
        messages.success(self.request, 'New post has beed registered.')
        return resolve_url('myapp:index')
    

class PostDetail(DetailView):
    model = Post
    template_name = 'myapp/post_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        is_liked = Like.objects.filter(user = self.request.user).filter(post = context['object'].pk).count() > 0
        context['is_liked'] = is_liked
        return context


class PostUpdate(OnlyMyPostMixin, UpdateView):
    model = Post
    form_class = PostForm 
    
    def get_success_url(self):
        messages.info(self.request, 'The Post has been updated.')
        return resolve_url('myapp:post_detail', pk=self.kwargs['pk'])
    
    
    
class PostDelete(OnlyMyPostMixin, DeleteView):
    model = Post
    
    def get_success_url(self):
        messages.info(self.request, 'The Post has been deleted.')
        return resolve_url('myapp:index')
    
    
class PostList(ListView):
    model = Post
    
    def get_queryset(self):
        return Post.objects.all().order_by('-created_at')
    
    
class Login(LoginView):
    form_class = LoginForm
    template_name = 'myapp/login.html'

    
class Logout(LogoutView):
    template_name = 'myapp/logout.html'
    
    
class SignUp(CreateView):
    form_class = SignUpForm
    template_name = 'myapp/signup.html'
    success_url = reverse_lazy('myapp:index')
    
    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        self.object = user
        messages.info(self.request, 'Your account has registered successfully.')
        return HttpResponseRedirect(self.get_success_url())


@login_required
def AddLike(request, post_id):
    post = Post.objects.get(id = post_id)
    is_liked = Like.objects.filter(user = request.user).filter(post = post_id).count()
    if is_liked > 0:
        messages.info(request, 'You already liked this post.')
    else:
        like = Like()
        like.user = request.user
        like.post = post
        like.save()
        messages.success(request, 'Added your liked articles!')
    return redirect('myapp:post_detail', post.id)