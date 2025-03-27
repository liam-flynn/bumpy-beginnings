from django.urls import include, path
from . import views
from .views import ArticleListView


urlpatterns = [
    path('', ArticleListView.as_view(), name='articles'),
    path('new/', views.create_article, name='create_article'),
    path('<int:article_id>/view/', views.view_article, name='view_article'),
    path('<int:article_id>/delete/', views.delete_article, name='delete_article'),
    path('<int:article_id>/edit/', views.edit_article, name='edit_article'),
    path('articles/', views.user_articles, name='user_articles'),
]
