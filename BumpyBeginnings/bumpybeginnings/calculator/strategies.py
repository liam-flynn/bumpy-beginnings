import hypothesis.strategies as st
import string
from django.utils.timezone import now
from django.contrib.auth.models import User
from users.models import SiteUser
from datetime import timedelta

benefit_name_strategy = st.text(
    alphabet=string.printable, min_size=1, max_size=255
).filter(lambda s: s.strip() != "")

benefit_description_strategy = st.text(
    alphabet=string.printable,
    min_size=1,
    max_size=500
).filter(lambda s: s.strip() != "")

criteria_description_strategy = st.text(
    alphabet=string.printable,
    min_size=1,
    max_size=500
).filter(lambda s: s.strip() != "")


frequency_strategy = st.sampled_from(["once", "weekly", "monthly", "annually"])

decimal_strategy = st.floats(
    min_value=0.01, max_value=1000, allow_nan=False, allow_infinity=False)

effective_date_value = now().date().isoformat()

criterion_strategy = st.text(
    alphabet=string.printable, min_size=1, max_size=100).filter(lambda s: s.strip() != "")

criteria_description_strategy = st.text(
    alphabet=string.printable,
    min_size=1,
    max_size=500
).filter(lambda s: s.strip() != "")
value_type_strategy = st.sampled_from(["boolean", "numeric", "text"])
match_type_strategy = st.sampled_from(["exact", "gt", "lt", "none"])


decimal_strategy = st.floats(
    min_value=0.01,
    max_value=1000,
    allow_nan=False,
    allow_infinity=False
)

reduction_rate_strategy = st.floats(
    min_value=0.01, max_value=100, allow_nan=False, allow_infinity=False)

effective_date_value = now().date().isoformat()


def value_strategy(match_type):
    if match_type == "none":
        return st.just("")
    else:
        return st.text(alphabet=string.printable, min_size=1, max_size=100).filter(lambda s: s.strip() != "")


def create_staff_user(username="staff", password="password"):
    return User.objects.create_user(username=username, password=password, is_staff=True)


def create_siteuser(user, isForumMod=False):
    return SiteUser.objects.create(user=user, dueDate=now().date() + timedelta(days=30), isForumMod=isForumMod)
