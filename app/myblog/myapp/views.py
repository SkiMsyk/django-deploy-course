from django.utils import timezone
from django.shortcuts import render, resolve_url
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import TemplateView, CreateView, DetailView, UpdateView, DeleteView, ListView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import login

from .models import Post
from .forms import PostForm, LoginForm, SignUpForm


class Index(TemplateView):
    template_name = 'myapp/index.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        post_list = Post.objects.all().order_by('-created_at')
        context = {
            'post_list': post_list,
        }
        return context
    
    
class PostCreate(CreateView):
    model = Post
    form_class = PostForm
    success_url = reverse_lazy('myapp:index')
    template_name = 'myapp/post_form.html'
    

class PostDetail(DetailView):
    model = Post
    template_name = 'myapp/post_detail.html'


class PostUpdate(UpdateView):
    model = Post
    form_class = PostForm 
    
    def get_success_url(self):
        messages.info(self.request, 'The Post has been updated.')
        return resolve_url('myapp:post_detail', pk=self.kwargs['pk'])
    
    
    
class PostDelete(DeleteView):
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
    