from asyncio.windows_events import NULL
from gc import get_objects
from re import template
from unicodedata import category
from urllib import response
import django
from django.shortcuts import render
from django.views.generic import ListView , DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Post, Category
from django.core.exceptions import PermissionDenied

class PostList(ListView): #포스트 목록 페이지
    model = Post
    ordering = '-pk' #최신 글 순서대로

    def get_context_data(self, **kwargs):
        context = super(PostList, self).get_context_data()
        context['categories'] = Category.objects.all() #카테고리 있을 경우 카운트 같은거
        context['no_category_post_count'] = Post.objects.filter(category=None).count() #카테고리 없는 미분류 항목
        return context

class PostDetail(DetailView): #포스트 상세 페이지
    model = Post

    def get_context_data(self, **kwargs):
        context = super(PostDetail, self).get_context_data()
        context['categories'] = Category.objects.all() #카테고리 있을 경우 카운트 같은거
        context['no_category_post_count'] = Post.objects.filter(category=None).count() #카테고리 없는 미분류 항목
        return context

class PostCreate(CreateView):
    model = Post
    
    fields = ['title', 'hook_text', 'content', 'head_image', 'head_video', 'category']

    def form_valid(self, form): # 로그인 = 작성자 확인
        current_user = self.request.user
        if current_user.is_authenticated:
            form.instance.author = current_user #로그인 되어있으면 얘로 보내줌
            return super(PostCreate, self).form_valid(form) #폼 리턴
        else: #로그인 하지 않은 회원이면
            return super(PostCreate, self).form_valid(form)

    # def form_valid(self, form): # 로그인 = 작성자 확인
    #     current_user = self.request.user
    #     if current_user.is_authenticated:
    #         form.instance.author = current_user #로그인 되어있으면 얘로 보내줌
    #         return super(PostCreate, self).form_valid(form) #폼 리턴
    #     else: #로그인 하지 않은 회원이면
    #         response = super(PostCreate, self).form_valid(form)
    #         id_str = self.request.POST.get('id_str')
    #         if id_str:
    #             form.instance.author = id_str
    #         return response

class PostUpdate(LoginRequiredMixin, UpdateView): #포스트 수정 기능
    model = Post

    fields = ['title', 'hook_text', 'content', 'head_image', 'head_video', 'category']

    template_name = 'player/post_update_form.html'

    def dispatch(self, request, *args, **kwargs) :
        if request.user.is_authenticated and request.user == self.get_object().author:
            return super(PostUpdate, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied #로그인 한 회원과 사용자가 일치하지 않을 경우 허가 거부 


def category_page(request, slug): #카테고리 분류 페이지
        #category = Category.objects.get(slug=slug)
        if slug == 'no_category' :
            category = '미분류'
            post_list = Post.objects.filter(category=None)
        else:
            category = Category.objects.get(slug=slug)
            post_list = Post.objects.filter(category=category)

        return render(
            request,
            'player/post_list.html',
            {
                'post_list' : post_list,
                'categories' : Category.objects.all(),
                'no_category_post_count' : Post.objects.filter(category=None).count(),
                'category' : category,
            }
        )