from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponseRedirect
from .models import Notification



@login_required
# get a list of all the users notitications
def Notifications(request):
    notifications = Notification.objects.filter(recipient=request.user).order_by('-timestamp')
    return render(request, 'notifications_dropdown.html', {'notifications': notifications})

# mark the notification as read
def mark_as_read(request, id):

    notification = get_object_or_404(Notification, id=id, recipient=request.user)
    
    if not notification.is_read:
        notification.mark_as_read()

    referer_url = request.META.get('HTTP_REFERER', '/')
    return HttpResponseRedirect(referer_url)