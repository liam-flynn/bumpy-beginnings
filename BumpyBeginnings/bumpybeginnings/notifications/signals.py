from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from forum.models import Comment, Vote
from .models import Notification

# create a new notification every time a new comment is created
@receiver(post_save, sender=Comment)
def comment_created(sender, instance, created, **kwargs):
    if created:
        recipient = instance.post.poster
        message = f"{instance.commenter.username} has commented on your post '{instance.post.postTitle}'"
        Notification.objects.create(recipient=recipient, notification_message=message)


@receiver(pre_save, sender=Vote)
def flag_vote_type_change(sender, instance, **kwargs):

    # when loading from a fixture (votes_data.json), import it as is.
    # don't try to match with data that might not be loaded yet.
    # https://docs.djangoproject.com/en/5.1/topics/db/fixtures/
    if kwargs["raw"]:
        return
    # check if the vote already existed
    if instance.pk:
        previous = Vote.objects.get(pk=instance.pk)
        # flag if the previous vote_type was empty and now it's "upvote"
        if not previous.vote_type and instance.vote_type and instance.vote_type.lower() == "upvote":
            instance._trigger_notification = True
    else:
        # for new instances, if vote_type is already "upvote", flag it.
        if instance.vote_type and instance.vote_type.lower() == "upvote":
            instance._trigger_notification = True

@receiver(post_save, sender=Vote)
def comment_upvote(sender, instance, created, **kwargs):
    postTitle = instance.comment.post.postTitle
    recipient = instance.comment.commenter
    message = f"Your comment in '{postTitle}' just received an upvote!"
    # for a newly created vote, if vote_type is "upvote"
    if created and instance.vote_type and instance.vote_type.lower() == "upvote":
        Notification.objects.create(recipient=recipient, notification_message=message)
    # for an update, check if our pre_save flagged the change.
    elif not created and getattr(instance, '_trigger_notification', False):
        Notification.objects.create(recipient=recipient, notification_message=message)