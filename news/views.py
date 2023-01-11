import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin

from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from .models import Post, Category
from .filters import PostFilter
from .forms import PostForm
from django.conf import settings


class PostList(ListView):
    model = Post
    ordering = '-datatime_of_creation'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        limit = settings.DAILY_POST_LIMIT
        today = datetime.datetime.now()
        limit_period = today - datetime.timedelta(days=1)

        posts_count_in_limit_period = Post.objects.filter(
            datatime_of_creation__gte=limit_period,
            author__authorUser=user,
        ).count()

        context['posts_in_limit_period'] = limit <= posts_count_in_limit_period

        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'


class PostSearch(ListView):
    model = Post
    ordering = 'heading'
    template_name = 'search.html'
    context_object_name = 'posts'

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class PostCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post',)
    model = Post
    template_name = 'post_create.html'
    form_class = PostForm

    def form_valid(self, form):
        post = form.save(commit=False)
        post.choices = 'NW'
        return super().form_valid(form)


class PostUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post',)
    model = Post
    template_name = 'post_create.html'
    form_class = PostForm


class PostDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('news.delete_post',)
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('posts')


class ArticlesCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_articles',)
    model = Post
    template_name = 'articles_create.html'
    form_class = PostForm

    def form_valid(self, form):
        post = form.save(commit=False)
        post.choices = 'PR'
        return super().form_valid(form)


class ArticlesUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_articles',)
    model = Post
    template_name = 'articles_create.html'
    form_class = PostForm


class ArticlesDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('news.delete_articles',)
    model = Post
    template_name = 'articles_delete.html'
    success_url = reverse_lazy('posts')


class CategoryListView(ListView):
    model = Post
    template_name = 'category_list.html'
    context_object_name = 'category_news_list'

    def get_queryset(self):
        self.category = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = Post.objects.filter(category=self.category).order_by('-datatime_of_creation')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_subscriber'] = self.request.user not in self.category.subscribers.all()
        context['category'] = self.category
        return context


@login_required
def subscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.add(user)

    message = 'Вы успешно подписались на рассылку новостей данной категории'
    return render(request, 'subscribe.html', {'category': category, 'message': message})
