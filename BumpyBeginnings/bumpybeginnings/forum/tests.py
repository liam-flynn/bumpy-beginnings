import json
from django.urls import reverse
from django.contrib.auth.models import User
from forum.models import Forum, Post, Comment
from hypothesis import given, settings
from hypothesis.strategies import text
from hypothesis.extra.django import TestCase as HypothesisTestCase
from hypothesis import given, strategies as st
from hypothesis.strategies import text
from .strategies import description_strategy, create_unique_forum, create_post, create_comment, unique_forum_name_strategy
from users.strategies import create_siteuser


class ForumViewTests(HypothesisTestCase):
    # test staff v user forum visibility. Staff members can see inactive forums
    def test_forum_list_view_staff_and_non_staff(self):
        # create accounts for staff and users
        staff = User.objects.create_user(
            username="staff", password="password", is_staff=True)
        user = User.objects.create_user(
            username="user", password="password", is_staff=False)
        # create a live and not live forum
        Forum.objects.create(forumName="Live Forum", isLive=True)
        Forum.objects.create(forumName="Not Live Forum", isLive=False)

        # login as the user, check to see if all forums they can see are live
        self.client.login(username="user", password="password")
        response = self.client.get(reverse('forum_list'))
        self.assertEqual(response.status_code, 200)
        forums = response.context["object_list"]
        self.assertTrue(all(forum.isLive for forum in forums))
        self.client.logout()

        # login as staff member. check to see that they can see 1 or more inactive forums
        self.client.login(username="staff", password="password")
        response = self.client.get(reverse('forum_list'))
        self.assertEqual(response.status_code, 200)
        forums = response.context["object_list"]
        inactive_forums = [forum for forum in forums if not forum.isLive]
        self.assertTrue(len(inactive_forums) >= 1)

    @settings(deadline=1000)
    @given(forum_name=unique_forum_name_strategy(), description=description_strategy)
    # check to see if staff can create new forums
    def test_create_forum_view(self, forum_name, description):
        # create a new staff member and login
        staff = User.objects.create_user(
            username="staff_create", password="password", is_staff=True)
        self.client.login(username="staff_create", password="password")
        # pass the data to the view
        data = {
            'forumName': forum_name,
            'description': description,
            'isLive': True
        }
        response = self.client.post(reverse('create_forum'), data)
        # expect a redirecton successful creation.
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Forum.objects.filter(
            forumName=forum_name.strip()).exists())

    def test_delete_forum_view(self):
        # create a new staff member and login
        staff = User.objects.create_user(
            username="staff_delete", password="password", is_staff=True)
        self.client.login(username="staff_delete", password="password")
        # create a new forum and pass it's id to the "delete_forum" view
        forum = create_unique_forum()
        url = reverse('delete_forum', kwargs={'forum_id': forum.id})
        # check to make sure forum has been deleted
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        with self.assertRaises(Forum.DoesNotExist):
            Forum.objects.get(id=forum.id)

    def test_deactivate_forum_view(self):
        # create a new staff member and login
        staff = User.objects.create_user(
            username="staff_deactivate", password="password", is_staff=True)
        self.client.login(username="staff_deactivate", password="password")
        # create a new forum and pass it's id to the "deactivate_forum" view
        forum = Forum.objects.create(forumName="Deactivate Forum", isLive=True)
        url = reverse('deactivate_forum', kwargs={'forum_id': forum.id})
        # check to make sure the forum is no longer live
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        forum.refresh_from_db()
        self.assertFalse(forum.isLive)

    def test_reactivate_forum_view(self):
        # create a new staff member and login
        staff = User.objects.create_user(
            username="staff_reactivate", password="password", is_staff=True)
        self.client.login(username="staff_reactivate", password="password")
        # create a new forum and pass it's id to the "Reactivate Forum" view
        forum = Forum.objects.create(
            forumName="Reactivate Forum", isLive=False)
        url = reverse('reactivate_forum', kwargs={'forum_id': forum.id})
        # check to make sure the forum is live
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        forum.refresh_from_db()
        self.assertTrue(forum.isLive)

    @settings(deadline=1000)
    @given(post_title=text(min_size=1, max_size=255), post_text=text())
    def test_post_creation(self, post_title, post_text):
        # create a forum first that will hold the post
        forum = create_unique_forum()
        forum.isLive = True
        forum.save()
        # create a user that will be our "poster"
        user = User.objects.create_user(
            username="user_post", password="password")
        self.client.login(username="user_post", password="password")
        url = reverse('forum_detail', kwargs={'pk': forum.id})
        # pass thepost details to the view
        post_title = "Test Post"
        post_text = "This is a test post."
        response = self.client.post(
            url, {'postTitle': post_title, 'postText': post_text})
        # check to make sure the post has been created and it is linked to our user
        self.assertEqual(response.status_code, 302)
        post = forum.posts.filter(postTitle=post_title).first()
        self.assertIsNotNone(post)
        self.assertEqual(post.poster, user)

    def test_delete_post_authorised(self):
        # create a poster user
        poster = User.objects.create_user(
            username="poster_auth", password="password")
        create_siteuser(poster)
        # create a forum for the post
        forum = create_unique_forum()
        forum.isLive = True
        forum.save()
        # create the post we want to delete
        post = create_post(
            forum, poster, postTitle="Delete Authorised", postText="Test")
        # login as the poster and confirm we can delete the post
        self.client.login(username="poster_auth", password="password")
        response = self.client.get(
            reverse('delete_post', kwargs={'pk': post.id}))
        self.assertEqual(response.status_code, 302)
        with self.assertRaises(Post.DoesNotExist):
            Post.objects.get(id=post.id)

    def test_delete_comment_authorised(self):
        # create a user for creating post and comment
        user = User.objects.create_user(
            username="user_delcomment", password="password")
        create_siteuser(user)
        # create aforum
        forum = create_unique_forum()
        forum.isLive = True
        forum.save()
        # create a post
        post = create_post(
            forum, user, postTitle="Comment Delete", postText="Test")
        # create a comment
        comment = create_comment(
            post, user, commentText="Delete this comment", score=0)
        # login as the commentor and check to see comment can be deleted
        self.client.login(username="user_delcomment", password="password")
        url = reverse('delete_comment', kwargs={'pk': comment.id})
        # for comment deletion we use the referer as comments can also be deleted from dashboard
        response = self.client.get(url, HTTP_REFERER='/')
        self.assertEqual(response.status_code, 302)
        with self.assertRaises(Comment.DoesNotExist):
            Comment.objects.get(id=comment.id)

    def test_upvote_comment_view(self):
        # create a voter and a commentor
        voter = User.objects.create_user(username="voter", password="password")
        commentor = User.objects.create_user(
            username="commentor", password="password")
        # create a forum / post / comment
        forum = create_unique_forum()
        forum.isLive = True
        forum.save()
        post = create_post(
            forum, commentor, postTitle="Upvote Test", postText="Test")
        comment = create_comment(
            post, commentor, commentText="Upvote me", score=0)
        # login as the voter
        self.client.login(username="voter", password="password")
        # try to upvote the comment using its id
        url = reverse('upvote_comment', kwargs={'comment_id': comment.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        # extract the data from the json content check it
        data = json.loads(response.content)
        self.assertEqual(data.get("score"), comment.score + 1)

    def test_downvote_comment_view(self):
        # create a voter and a commentor
        voter = User.objects.create_user(username="voter", password="password")
        commentor = User.objects.create_user(
            username="commentor", password="password")

        # create a forum / post / comment
        forum = create_unique_forum()
        forum.isLive = True
        forum.save()
        post = create_post(
            forum, commentor, postTitle="Downvote Test", postText="Test")
        comment = create_comment(
            post, commentor, commentText="Downvote me", score=0)

        # login as the voter
        self.client.login(username="voter", password="password")

        # try to upvote the comment using its id
        url = reverse('downvote_comment', kwargs={'comment_id': comment.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        # extract the data from the json content check it
        data = json.loads(response.content)
        self.assertEqual(data.get("score"), comment.score - 1)

    def test_low_score_comments_view(self):
        # create a staff user and a poster
        staff = User.objects.create_user(
            username="staff", password="password", is_staff=True)
        poster = User.objects.create_user(
            username="poster", password="password")

        # create a forum and post
        forum = create_unique_forum()
        forum.isLive = True
        forum.save()
        post = create_post(
            forum, poster, postTitle="Test Post", postText="Test")

        # create high and low scoring comments
        low_comment = create_comment(
            post, poster, commentText="Low score comment", score=-3)
        high_comment = create_comment(
            post, poster, commentText="High score comment", score=3)

        # login as staff member
        self.client.login(username="staff", password="password")

        # access the "low_score_comments" view
        url = reverse('low_score_comments')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        # check to make sure the low score comment is in list and high is not
        comments = response.context["comments"]
        self.assertIn(low_comment, comments)
        self.assertNotIn(high_comment, comments)
