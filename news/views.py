from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Post
from .filters import PostFilter
from .forms import PostForm


class PostList(ListView):
    model = Post
    ordering = '-datatime_of_creation'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 10


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
    permission_required = ('news.post_create')
    model = Post
    template_name = 'post_create.html'
    form_class = PostForm

    def form_valid(self, form):
        post = form.save(commit=False)
        post.choices = 'NW'
        return super().form_valid(form)


class PostUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.post_update')
    model = Post
    template_name = 'post_create.html'
    form_class = PostForm


class PostDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('news.post_delete')
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('posts')


class ArticlesCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('news.articles_create')
    model = Post
    template_name = 'articles_create.html'
    form_class = PostForm

    def form_valid(self, form):
        post = form.save(commit=False)
        post.choices = 'PR'
        return super().form_valid(form)


class ArticlesUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.articles_update')
    model = Post
    template_name = 'articles_create.html'
    form_class = PostForm


class ArticlesDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('news.articles_update')
    model = Post
    template_name = 'articles_delete.html'
    success_url = reverse_lazy('posts')

