from hypothesis.extra.django import TestCase as HypothesisTestCase
from hypothesis import given, strategies as st
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils.timezone import now
from .models import Article
from datetime import timedelta
from hypothesis import settings
from .strategies import article_strategy
from users.strategies import site_user_strategy


class ArticleViewsTest(HypothesisTestCase):
    # test ArticleListView
    def test_article_list_view(self):
        # make a admin account as only admins can access articles.html
        self.client.force_login(User.objects.create_superuser("admin", "admin@bumpybeginnings.co.uk", "password"))
        response = self.client.get(reverse("articles"))
        self.assertEqual(response.status_code, 200)
        # verify that the correct template was used and it included the object_list (articles)
        self.assertTemplateUsed(response, "articles.html")
        self.assertIn("object_list", response.context)

    # test "Create Article" view
    @given(article=article_strategy)
    def test_create_article_view(self, article):
        self.client.force_login(User.objects.create_superuser("admin", "admin@bumpybeginnings.co.uk", "password"))
        # prepare the POST data from the article strategy
        post_data = {
            "title": article.title,
            "subtitle": article.subtitle,
            "text": article.text,
            "source": article.source if article.source is not None else '',
        }
        # add `related_week` only if it is not None
        if article.related_week is not None:
            post_data["related_week"] = article.related_week

        response = self.client.post(reverse("create_article"), post_data)
        # redirect after success
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Article.objects.filter(title=article.title).exists())

    # test "View Article" view
    @given(article=article_strategy)
    def test_view_article_view(self, article):
        # save the generated article to the database
        article.save()
        # try to view the article using the article id
        response = self.client.get(reverse("view_article", kwargs={"article_id": article.id}))
        # check to make sure the response is ok and the correct template has been used
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "view_article.html")
        self.assertEqual(response.context["article"], article)

    # test "Edit Article" View
    @given(article=article_strategy)
    def test_edit_article_view(self, article):
        self.client.force_login(User.objects.create_superuser("admin", "admin@bumpybeginnings.co.uk", "password"))
        # save the article to the database
        article.save()  
        # strip any trailing whitespace
        updated_title = "Updated " + article.title.strip()
        # prepare post data
        post_data = {
            "title": updated_title,
            "subtitle": article.subtitle,
            "text": article.text,
            "source": article.source if article.source is not None else "", 
            "related_week": article.related_week if article.related_week is not None else "",  
        }

        # send a post request to edit the article
        response = self.client.post(reverse("edit_article", kwargs={"article_id": article.id}), post_data)

        # check that a redirect happens after the amendment (back to the articles list)
        self.assertEqual(response.status_code, 302) 
        # reload the article from the database
        article.refresh_from_db()
        # ensure the article was updated
        self.assertEqual(article.title.strip(), updated_title)

    # test "Delete Article" View
    @settings(deadline=500)
    @given(article=article_strategy)
    def test_delete_article_view(self, article):
        self.client.force_login(User.objects.create_superuser("admin", "admin@bumpybeginnings.co.uk", "password"))
        # save the article to the database
        article.save()
        # check to see if the article can be deleted using the created article id
        response = self.client.post(reverse("delete_article", kwargs={"article_id": article.id}))
        # redirect on successful deletion
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Article.objects.filter(id=article.id).exists())

    # test User Articles View
    @given(site_user=site_user_strategy(), article=article_strategy)
    def test_user_articles_view(self, site_user, article):
        # set up the user and save
        site_user.user.save()
        # make the user be 12 weeks pregnant
        site_user.dueDate = now().date() + timedelta(weeks=40 - 12)
        site_user.save()

        # set up the article and save
        article.related_week = 12
        article.save()

        # log in the site user
        self.client.force_login(site_user.user)

        # make the request and check the response
        response = self.client.get(reverse("user_articles"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "user_articles.html")
        self.assertIn("articles", response.context)
        self.assertIn(article, response.context["articles"])