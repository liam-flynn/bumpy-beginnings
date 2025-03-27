from django.db import models
from django.contrib.auth.models import User
from django_bleach.models import BleachField
from notifications.models import Notification
from django.http import HttpRequest

# model for the high level data structure that contains posts


class Forum(models.Model):
    forumName = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    isLive = models.BooleanField(default=False)

    def __str__(self):
        return self.forumName

# user created posts where other users can leave comments


class Post(models.Model):
    forum = models.ForeignKey(
        Forum, on_delete=models.CASCADE, related_name="posts")
    poster = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="posts")
    postTitle = models.CharField(max_length=255)
    postText = BleachField(
        allowed_tags=['a', 'ul', 'ol', 'li', 'strong', 'em', 'u', 'p', 'br', 'span'])
    isActive = models.BooleanField(default=True)
    createdOn = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.postTitle

# comments that are available in posts


class Comment(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="comments")
    commenter = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="comments")
    createdOn = models.DateTimeField(auto_now_add=True)
    commentText = BleachField()
    score = models.IntegerField(default=0)

    # overridden logic to include notifying users when their comments have been deleted
    def delete(self, request: HttpRequest, *args, **kwargs):
        user = request.user
        if user != self.commenter:
            # notify the original commenter
            Notification.objects.create(
                recipient=self.commenter,
                notification_message=f"Your comment was removed by one of our moderators."
            )
        super().delete(*args, **kwargs)

    def __str__(self):
        return f"Comment by {self.commenter} on {self.createdOn}"

# model to store upvote and downvote records


class Vote(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="votes")
    comment = models.ForeignKey(
        Comment, on_delete=models.CASCADE, related_name="votes")
    vote_type = models.CharField(max_length=10, choices=(
        ('upvote', 'Upvote'), ('downvote', 'Downvote')))

    class Meta:
        # Ensure one vote per user per comment
        unique_together = ('user', 'comment')

    def __str__(self):
        return f"{self.user.username} {self.vote_type} on Comment {self.comment.id}"
