from django.shortcuts import render
from django.views.generic import ListView , DetailView
from .models import Post

class PostList(ListView):
    model = Post
    ordering = '-pk' #최신 글 순서대로

class PostDetail(DetailView):
    model = Post