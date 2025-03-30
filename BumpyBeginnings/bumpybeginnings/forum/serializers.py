from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Forum, Post, Comment, Vote

# serialisers for forum models


class ForumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Forum
        fields = ['id', 'forumName', 'description', 'isLive']


class PostSerializer(serializers.ModelSerializer):
    forum = serializers.PrimaryKeyRelatedField(queryset=Forum.objects.all())
    poster = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Post
        fields = ['id', 'forum', 'poster', 'postTitle',
                  'postText', 'isActive', 'createdOn']
        read_only_fields = ['createdOn']


class CommentSerializer(serializers.ModelSerializer):
    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all())
    commenter = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Comment
        fields = ['id', 'post', 'commenter',
                  'createdOn', 'commentText', 'score']
        read_only_fields = ['createdOn', 'score']


class VoteSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    comment = serializers.PrimaryKeyRelatedField(
        queryset=Comment.objects.all())

    class Meta:
        model = Vote
        fields = ['id', 'user', 'comment', 'vote_type']
