from asyncio.windows_events import NULL
from unicodedata import category
from django.shortcuts import render
from django.views.generic import ListView , DetailView, CreateView, UpdateView
from .models import Post, Category

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
            form.instance.author = current_user
            return super(PostCreate, self).form_valid(form)
        else: #로그인 하지 않은 회원이면
            return super(PostCreate, self).form_valid(form)

# class PostUpdate(LoginRequiredMixin, UpdateView):
#     model = Post
#     fields = ['title', 'hook_text', 'content', 'head_image', 'head_video', 'category']

#     def form_valid(self, form): # 로그인 = 작성자 확인
#         current_user = self.request.user
#         if current_user.is_authenticated:
#             form.instance.author = current_user
#             return super(PostCreate, self).form_valid(form)
#         else: #로그인 하지 않은 회원이면
#             return super(PostCreate, self).form_valid(form)

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