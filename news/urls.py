from django.urls import path
from .views import PostList, PostDetail, PostCreate, PostSearch, PostUpdate, PostDelete, ArticlesCreate, \
   ArticlesUpdate, ArticlesDelete


urlpatterns = [
   path('news/', PostList.as_view(), name='posts'),
   path('news/<int:pk>', PostDetail.as_view(), name='post'),
   path('news/search/', PostSearch.as_view(), name='search'),
   path('news/create/', PostCreate.as_view(), name='post_create'),
   path('news/<int:pk>/update/', PostUpdate.as_view(), name='post_update'),
   path('news/<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
   path('articles/create/', ArticlesCreate.as_view(), name='articles_create'),
   path('articles/<int:pk>/update/', ArticlesUpdate.as_view(), name='articles_update'),
   path('articles/<int:pk>/delete/', ArticlesDelete.as_view(), name='articles_delete'),

]
