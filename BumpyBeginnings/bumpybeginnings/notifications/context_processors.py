from .models import Notification

# context processor so all templates have access to notifications
# help from https://www.horilla.com/blogs/how-to-implement-context-processors-in-django/


def notifications_processor(request):
    if request.user.is_authenticated:
        notifications = Notification.objects.filter(
            recipient=request.user).order_by('-timestamp')
        unread_count = notifications.filter(is_read=False).count()
    else:
        notifications = []
        unread_count = 0
    return {'notifications': notifications,
            'unread_count': unread_count,
            }
