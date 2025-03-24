from django.urls import reverse
from rest_framework.test import APIRequestFactory, force_authenticate
from hypothesis import given
from hypothesis.extra.django import from_model
from django.contrib.auth.models import User
from forum.models import Forum
from .views import (
    ArticleViewSet, ForumViewSet, PostViewSet, CommentViewSet,
    VoteViewSet, DevelopmentMilestoneViewSet, SiteUserViewSet
)
from articles.strategies import article_strategy
from forum.strategies import comment_strategy, forum_strategy, post_strategy, vote_strategy
from tracker.strategies import development_milestone_strategy
from users.strategies import site_user_strategy
from hypothesis.extra.django import TestCase as HypothesisTestCase


# setup test client used for each test i.e. API access is admin only. initialised once / not every test
# help from https://dzone.com/articles/python-unit-testing-one-time-initialization
class APITestSetup(HypothesisTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # create the APIRequest factory wee will use to build mock requests
        cls.factory = APIRequestFactory()
        # get or create a admin user for authenication requests
        cls.user, created = User.objects.get_or_create(
            username='admin',
            defaults={'email': 'admin@bumpybeginnings.co.uk', 'is_superuser': True, 'is_staff': True}
        )
        # if we didn't already have a user and one created, add in the password.
        if created:
            cls.user.set_password('password')
            cls.user.save()


# tests for the article API endpoints
class ArticleViewSetTest(APITestSetup):
    @given(article=article_strategy)
    def test_list_articles(self, article):
        # save the article so it is in the database
        article.save()
        # get the listview for articles
        view = ArticleViewSet.as_view({'get': 'list'})
        # create a GET request to the article list url
        request = self.factory.get(reverse('article-list'))
        # force authorisation for the request using the admin user
        force_authenticate(request, user=self.user)
        # call the view with the request
        response = view(request)
        # assert the repsonse status is OK(200)
        self.assertEqual(response.status_code, 200)

    @given(article=article_strategy)
    def test_retrieve_article(self, article):
        # make sure the generated strings from the strategy are valid charactors
        article.text = str(article.text)
        article.save()
        # get the 'retrieve' view for that article
        view = ArticleViewSet.as_view({'get': 'retrieve'})
        # create a GET request to the article detail URL using the pk of what we just created
        request = self.factory.get(reverse('article-detail', args=[article.pk]))
        force_authenticate(request, user=self.user)
        response = view(request, pk=article.pk)
        # assert that the response status code is 200 and the id matches.
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['id'], article.id)

# tests for the Forum API endpoints
class ForumViewSetTest(APITestSetup):
    @given(forum=from_model(Forum))
    def test_list_forums(self, forum):
        # save the forum instance
        forum.save()
        # create a GET request to the article list url
        view = ForumViewSet.as_view({'get': 'list'})
        request = self.factory.get(reverse('forum-list'))
        force_authenticate(request, user=self.user)
        # assert that we get a 200 OK response
        response = view(request)
        self.assertEqual(response.status_code, 200)

    @given(forum=forum_strategy())
    def test_retrieve_forum(self, forum):
        forum.save()
        # get the 'retrieve' view for that forum
        view = ForumViewSet.as_view({'get': 'retrieve'})
        request = self.factory.get(reverse('forum-detail', args=[forum.pk]))
        force_authenticate(request, user=self.user)
        # call the view with the request and pass the pk as a parameter
        response = view(request, pk=forum.pk)
        # assert that the response status code is 200 and the id matches.
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['id'], forum.id)

# tests for the forum posts API endpoint
class PostViewSetTest(APITestSetup):
    @given(post=post_strategy())
    def test_list_posts(self, post):
        # save the post so it is in the database
        post.save()
        # get the 'list' view for posts
        view = PostViewSet.as_view({'get': 'list'})
        request = self.factory.get(reverse('post-list'))
        force_authenticate(request, user=self.user)
        # assert that we get a 200 OK response
        response = view(request)
        self.assertEqual(response.status_code, 200)

# tests for the comment API endpoints
class CommentViewSetTest(APITestSetup):
    @given(comment=comment_strategy())
    def test_list_comments(self, comment):
        # save the comment so it is in the database
        comment.save()
        # get the 'list' view for comments
        view = CommentViewSet.as_view({'get': 'list'})
        request = self.factory.get(reverse('comment-list'))
        force_authenticate(request, user=self.user)
        # assert that we get a 200 OK response
        response = view(request)
        self.assertEqual(response.status_code, 200)

class VoteViewSetTest(APITestSetup):
    @given(vote=vote_strategy())
    def test_list_votes(self, vote):
        # save the vote so it is in the database
        vote.save()
        # get the 'list' view for votes
        view = VoteViewSet.as_view({'get': 'list'})
        request = self.factory.get(reverse('vote-list'))
        force_authenticate(request, user=self.user)
        # assert that we get a 200 OK response
        response = view(request)
        self.assertEqual(response.status_code, 200)

# tests for the development milestones API endpoint 
class DevelopmentMilestoneViewSetTest(APITestSetup):
    @given(milestone=development_milestone_strategy())
    def test_list_milestones(self, milestone):
        # save the development milestone it is in the database
        milestone.save()
        # get the 'list' view for milestones
        view = DevelopmentMilestoneViewSet.as_view({'get': 'list'})
        request = self.factory.get(reverse('milestone-list'))
        force_authenticate(request, user=self.user)
        # assert that the API returns HTTP 200 OK
        response = view(request)
        self.assertEqual(response.status_code, 200)

# tests for site user API endpoint
class SiteUserViewSetTest(APITestSetup):
    @given(user=site_user_strategy())
    def test_list_siteusers(self, user):
        # save the vote so it is in the database
        user.save()
        # get the 'list' view for site users
        view = SiteUserViewSet.as_view({'get': 'list'})
        request = self.factory.get(reverse('siteuser-list'))
        force_authenticate(request,         user=self.user)
        # assert that the API returns HTTP 200 OK
        response = view(request)
        self.assertEqual(response.status_code, 200)