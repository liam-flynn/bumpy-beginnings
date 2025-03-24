from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from hypothesis import given, strategies as st
from hypothesis.extra.django import TestCase as HypothesisTestCase
from .models import SiteUser
from hypothesis import settings
from .strategies import site_user_strategy, user_strategy

class UserViewsTest(HypothesisTestCase):
    # tst the get_details view
    @given(site_user=site_user_strategy())
    def test_get_details_view(self, site_user):
        self.client.force_login(site_user.user)
        # load the "get_details" page
        response = self.client.get(reverse('get_details'))

        if SiteUser.objects.filter(user=site_user.user).exists():
            # if user already has a SiteUser, they shoudl be redirected straight to the homepage
            self.assertEqual(response.status_code, 302)
            self.assertEqual(response.url, reverse('homepage'))
        else:
            # user does not have a SiteUser, they get sent to the "provide_details" page
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, 'provideDetails.html')

        # test form submission
        post_data = {
            'isMother': False,
            'dueDate': (timezone.now().date() + timezone.timedelta(days=100)).isoformat(),
            'partnerName': 'John Doe',
        }

        # pass the post data to the "get_details" page
        response = self.client.post(reverse('get_details'), data=post_data)
        # user should be redirected to homepage
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('homepage'))
        # the user should now have a corrisponding site user
        self.assertTrue(SiteUser.objects.filter(user=site_user.user).exists())

    # Test the homepage view
    @given(user=user_strategy)
    def test_homepage_view(self, user):
        # unauthenticated user
        response = self.client.get(reverse('homepage'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('login'))

        # Authenticated user
        self.client.force_login(user)
        response = self.client.get(reverse('homepage'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'homepage.html')

    # test the login view
    @settings(deadline=2000)
    @given(user=user_strategy)
    def test_login_view(self, user):
        user.set_password('password123!')
        user.save()

        # test valid login
        post_data = {'username': user.username, 'password': 'password123!'}
        response = self.client.post(reverse('login'), data=post_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('get_details'))

        # test invalid login
        post_data = {'username': user.username, 'password': 'wrong-password'}
        response = self.client.post(reverse('login'), data=post_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')
        self.assertContains(response, "Invalid login. Please try again.")

    # test the logout view
    @given(user=user_strategy)
    def test_logout_view(self, user):
        self.client.force_login(user)
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('homepage'))
