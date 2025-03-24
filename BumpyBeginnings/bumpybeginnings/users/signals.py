from django.dispatch import receiver
from allauth.account.signals import user_logged_in
from .models import SiteUser

@receiver(user_logged_in)
def ensure_user_details(sender, request, user, **kwargs):
    # Check if the user has the necessary details
    if not SiteUser.objects.filter(user=user).exists() and not user.is_staff:
        # Store a flag in the session to redirect them after login
        request.session['requires_details'] = True