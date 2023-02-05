import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin

from django.core.cache import cache
from django.shortcuts import get_object_or_404, render
from django.conf import settings
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, \
    ListView, UpdateView

from .filters import PostFilter
from .forms import PostForm
from .models import Category, Post


class PostList(ListView):
    """Класс обрабатывает список постов posts."""

    model = Post
    ordering = '-datatime_of_creation'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        """Метод ограничивает количество постов в день для одного автора. \
        Лимит DAILY_POST_LIMIT в settings.py."""
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
    """Класс обрабатывает конкретный пост Post."""

    model = Post
    template_name = 'post.html'
    context_object_name = 'post'

    def get_object(self, *args, **kwargs):
        """Метод кэширует post до тех пор, пока он не будет изменен\
        Удаление из кэша при изменении реализовано в models."""
        obj = cache.get(f'post-{self.kwargs["pk"]}', None)

        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'post-{self.kwargs["pk"]}', obj)

        return obj


class PostSearch(ListView):
    """Класс реализует поиск постов."""

    model = Post
    ordering = 'heading'
    template_name = 'search.html'
    context_object_name = 'posts'

    def get_queryset(self):
        """Переопределяем функцию получения списка постов\
        сохраняем фильтрацию PostFilter в объекте класса\
        и возвращаем отфильтрованный список."""
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        """Добавляем в контекст объект фильтрации."""
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class PostCreate(PermissionRequiredMixin, CreateView):
    """Представление для создания нового объекта Post, с choices=NEWS."""

    permission_required = ('news.add_post',)
    model = Post
    template_name = 'post_create.html'
    form_class = PostForm

    def form_valid(self, form):
        """Метод устанавливает поле choice модели post в положение NEWS."""
        post = form.save(commit=False)
        post.choices = 'NW'
        return super().form_valid(form)


class PostUpdate(PermissionRequiredMixin, UpdateView):
    """Представление для обновления объекта post."""

    permission_required = ('news.change_post',)
    model = Post
    template_name = 'post_create.html'
    form_class = PostForm


class PostDelete(PermissionRequiredMixin, DeleteView):
    """Представление для удаления объекта post."""

    permission_required = ('news.delete_post',)
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('posts')


class ArticlesCreate(PermissionRequiredMixin, CreateView):
    """Представление для создания нового объекта Post, с choices=PAPER."""

    permission_required = ('news.add_articles',)
    model = Post
    template_name = 'articles_create.html'
    form_class = PostForm

    def form_valid(self, form):
        """Метод устанавливает поле choice модели post в положение PAPER."""
        post = form.save(commit=False)
        post.choices = 'PR'
        return super().form_valid(form)


class ArticlesUpdate(PermissionRequiredMixin, UpdateView):
    """Представление для обновления объекта post."""

    permission_required = ('news.change_articles',)
    model = Post
    template_name = 'articles_create.html'
    form_class = PostForm


class ArticlesDelete(PermissionRequiredMixin, DeleteView):
    """Представление для удаления объекта post."""

    permission_required = ('news.delete_articles',)
    model = Post
    template_name = 'articles_delete.html'
    success_url = reverse_lazy('posts')


class CategoryListView(ListView):
    """Представление для создания списка постов Post \
    по одной категории Category."""

    model = Post
    template_name = 'category_list.html'
    context_object_name = 'category_news_list'

    def get_queryset(self):
        """Метод возвращает список постов выбранной категории."""
        self.category = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = Post.objects.filter(
            category=self.category
        ).order_by('-datatime_of_creation')
        return queryset

    def get_context_data(self, **kwargs):
        """Метод передает в контекст категорию и результат\
        проверки юзера на подписку к данной категории."""
        context = super().get_context_data(**kwargs)
        context['is_not_subscriber'] = self.request.user not in self.category.subscribers.all()
        context['category'] = self.category
        return context


@login_required
def subscribe(request, pk):
    """Метод реализует подписку к категории и отправку \
    сообщения об успешной подписке."""
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.add(user)

    message = 'Вы успешно подписались на рассылку новостей данной категории'
    return render(
        request, 'subscribe.html', {'category': category, 'message': message}
    )


@login_required
def unsubscribe(request, pk):
    """Метод реализует отказ от подписки к категории\
    и отправку сообщения об успешном прекращении подписки."""
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.remove(user)

    message = 'Вы успешно отписались от рассылки новостей данной категории'
    return render(
        request, 'subscribe.html', {'category': category, 'message': message}
    )
