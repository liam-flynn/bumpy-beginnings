from rest_framework.routers import DefaultRouter
from .views import ArticleViewSet,ForumViewSet, PostViewSet, CommentViewSet, VoteViewSet, NotificationViewSet, DevelopmentMilestoneViewSet, SiteUserViewSet
from django.urls import path, include
from rest_framework.authtoken import views


router = DefaultRouter()
# Register all viewsets with the router to automatically generate API endpoints for each resource.
router.register(r'articles', ArticleViewSet, basename='article')
router.register(r'forums', ForumViewSet, basename='forum')
router.register(r'posts', PostViewSet, basename='post')
router.register(r'comments', CommentViewSet, basename='comment')
router.register(r'vote', VoteViewSet, basename='vote')
router.register(r'notifications', NotificationViewSet, basename='notification')
router.register(r'milestones', DevelopmentMilestoneViewSet, basename='milestone')
router.register(r'siteusers', SiteUserViewSet, basename='siteuser')


# include all the automatically generated routes from the router at the root URL
urlpatterns = [
    path('', include(router.urls), name='swagger'),
    path('api-token-auth/', views.obtain_auth_token, name='api-token-auth'),
]