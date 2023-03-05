from django.urls import path
from django.views.decorators.cache import cache_page

from .views import ArticlesCreate, ArticlesDelete, ArticlesUpdate, \
   CategoryListView, PostCreate, PostDelete, PostDetail, PostList, \
   PostSearch, PostUpdate, subscribe, Time, unsubscribe


urlpatterns = [
   path(
      'news/',
      cache_page(60)(PostList.as_view()),
      name='posts'
   ),
   path(
      'news/<int:pk>',
      PostDetail.as_view(),
      name='post'
   ),
   path(
      'news/search/',
      PostSearch.as_view(),
      name='search'
   ),
   path(
      'news/create/',
      PostCreate.as_view(),
      name='post_create'
   ),
   path(
      'news/<int:pk>/update/',
      PostUpdate.as_view(),
      name='post_update'
   ),
   path(
      'news/<int:pk>/delete/',
      PostDelete.as_view(),
      name='post_delete'
   ),
   path(
      'articles/create/',
      ArticlesCreate.as_view(),
      name='articles_create'
   ),
   path(
      'articles/<int:pk>/update/',
      ArticlesUpdate.as_view(),
      name='articles_update'
   ),
   path(
      'articles/<int:pk>/delete/',
      ArticlesDelete.as_view(),
      name='articles_delete'
   ),
   path(
      'news/categories/<int:pk>',
      CategoryListView.as_view(),
      name='category_list'
   ),
   path(
      'news/categories/<int:pk>/subscribe',
      subscribe,
      name='subscribe'
   ),
   path(
      'news/categories/<int:pk>/unsubscribe',
      unsubscribe,
      name='unsubscribe'
   ),
   path(
      'news/time',
      Time.as_view(),
      name='time'
   ),
]
