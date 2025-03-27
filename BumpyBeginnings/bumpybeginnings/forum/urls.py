from django.urls import include, path
from . import views
from .views import ForumListView, ForumDetailView, PostDetailView


urlpatterns = [
    path('', ForumListView.as_view(), name='forum_list'),
    path('new/', views.create_forum, name='create_forum'),
    path('forums/<int:forum_id>/delete/',
         views.delete_forum, name='delete_forum'),
    path('forums/<int:forum_id>/deactivate/',
         views.deactivate_forum, name='deactivate_forum'),
    path('forums/<int:forum_id>/reactivate/',
         views.reactivate_forum, name='reactivate_forum'),
    path('<int:pk>/', ForumDetailView.as_view(), name='forum_detail'),
    path('<int:forum_id>/posts/<int:pk>/',
         PostDetailView.as_view(), name='post_detail'),
    path('posts/<int:pk>/delete/', views.delete_post, name='delete_post'),
    path('comments/<int:pk>/delete/', views.delete_comment, name='delete_comment'),
    path('comment/<int:comment_id>/upvote/',
         views.upvote_comment, name='upvote_comment'),
    path('comment/<int:comment_id>/downvote/',
         views.downvote_comment, name='downvote_comment'),
    path('low-score-comments/', views.low_score_comments, name='low_score_comments')
]
