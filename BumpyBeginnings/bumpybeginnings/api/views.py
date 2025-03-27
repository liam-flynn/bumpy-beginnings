from rest_framework import viewsets
from articles.models import Article
from articles.serializers import ArticleSerializer
from forum.models import Forum
from forum.serializers import ForumSerializer
from forum.models import Post
from forum.serializers import PostSerializer
from forum.models import Comment
from forum.serializers import CommentSerializer
from forum.models import Vote
from forum.serializers import VoteSerializer
from notifications.models import Notification
from notifications.serializers import NotificationSerializer
from tracker.models import DevelopmentMilestone
from tracker.serializers import DevelopmentMilestoneSerializer
from users.models import SiteUser
from users.serializers import SiteUserSerializer
from rest_framework.permissions import IsAdminUser

# define viewsets for handling CRUD operations on different resources.
# all endpoints are only available to admins


class ArticleViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()


class ForumViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = Forum.objects.all()
    serializer_class = ForumSerializer


class PostViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class CommentViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class VoteViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer


class NotificationViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer


class DevelopmentMilestoneViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = DevelopmentMilestone.objects.all()
    serializer_class = DevelopmentMilestoneSerializer


class SiteUserViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = SiteUser.objects.all()
    serializer_class = SiteUserSerializer
