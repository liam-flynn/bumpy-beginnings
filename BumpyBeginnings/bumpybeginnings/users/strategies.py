from hypothesis.extra.django import from_model
from .models import SiteUser
from django.contrib.auth.models import User
from django.utils import timezone
from hypothesis import strategies as st
from django.utils.timezone import now
from datetime import timedelta
from hypothesis.strategies import text, characters

# strategy to generate a User
user_strategy = from_model(User)



# strategy to generate a SiteUser, ensuring a related User is created
@st.composite
def site_user_strategy(draw, isForumMod=False):
    # Ensure unique User and SiteUser
    user = draw(from_model(User))
    partner_name = draw(
        text(characters(blacklist_characters='\x00'), min_size=1, max_size=80)
    )
    site_user, created = SiteUser.objects.get_or_create(
        user=user,
        defaults={
            "isMother": draw(st.booleans()),
            "dueDate": draw(st.dates(
                min_value=timezone.now().date(),
                max_value=timezone.now().date() + timezone.timedelta(days=365)
            )),
            "partnerName": partner_name,
            "isForumMod": isForumMod,
        },
    )
    return site_user



# method for creating a quick user, i.e. one required to create a comment
def create_siteuser(user, isForumMod=False):
    # Create a SiteUser for a given user.
    return SiteUser.objects.create(user=user, dueDate=now().date() + timedelta(days=30), isForumMod=isForumMod)