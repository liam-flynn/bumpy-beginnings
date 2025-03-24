from hypothesis.extra.django import TestCase as HypothesisTestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils.timezone import now
from .models import DevelopmentMilestone
from hypothesis import settings
from users.strategies import user_strategy, site_user_strategy
from .strategies import development_milestone_strategy
from hypothesis import given



class DevelopmentMilestoneViewsTest(HypothesisTestCase):
    # test Milestone List View
    def test_milestone_list_view(self):
        response = self.client.get(reverse("milestones"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "milestones.html")
        self.assertIn("object_list", response.context)

class DevelopmentMilestoneViewsTest(HypothesisTestCase):
    # test deleting a milestone
    @given(milestone=development_milestone_strategy())
    @settings(deadline=500)
    def test_delete_milestone_view(self, milestone):
        # create an admin user (admins can only delete milestones)
        self.client.force_login(User.objects.create_superuser("admin", "admin@bumpybeginnings.co.uk", "password"))
        milestone.save()
        # pass the milestone id to the "delete_milestone" view 
        response = self.client.post(reverse("delete_milestone", kwargs={"id": milestone.id}))
        # check there is a redirect on successful deletion
        self.assertEqual(response.status_code, 302)
        self.assertFalse(DevelopmentMilestone.objects.filter(id=milestone.id).exists())

    # test editting a milestone
    @given(milestone=development_milestone_strategy())
    @settings(deadline=500)
    def test_edit_milestone_view(self, milestone):
        # create a staff user
        user = User.objects.create_superuser("admin", "admin@bumpybeginnings.co.uk", "password")
        self.client.force_login(user)

        # save the milestone to the database
        milestone.save()

        # update the description
        updated_description = "Updated " + milestone.description

        post_data = {
            "stage": milestone.stage,
            "description": updated_description,
            "week": milestone.week if milestone.week is not None else "",
            "start_age_months": milestone.start_age_months if milestone.start_age_months is not None else "",
            "end_age_months": milestone.end_age_months if milestone.end_age_months is not None else "",
        }

        response = self.client.post(reverse("edit_milestone", kwargs={"id": milestone.id}), post_data)

        # check there is a redirect on success and milestone is now edited
        self.assertEqual(response.status_code, 302)
        milestone.refresh_from_db()
        self.assertEqual(milestone.description, updated_description)

    # test viewing a milestone
    @given(milestone=development_milestone_strategy())
    def test_view_milestone_view(self, milestone):
        # save the milestone
        milestone.save()
        # pass the milestone id to the "view_milestone" view
        response = self.client.get(reverse("view_milestone", kwargs={"id": milestone.id}))
        # check to make sure the page loads successfully, the correct template it used and the correct milestone
        # is being pulled through
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "view_milestone.html")
        self.assertEqual(response.context["milestone"], milestone)

    # test the correct milestone is being pulled through
    @given(site_user=site_user_strategy(), milestone=development_milestone_strategy())
    def test_get_current_milestone(self, site_user, milestone):
        # create a user
        site_user.user.save()
        site_user.save()
        # set the milestone stage depending on how the user's due date
        milestone.stage = "prenatal" if site_user.dueDate > now().date() else "postnatal"
        milestone.save()
        # login as the user
        self.client.force_login(site_user.user)
        response = self.client.get(reverse("user_milestone"))
        # check to make sure the correct milestone is being pulled through via the correct template
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "milestone.html")
        self.assertIn("milestone", response.context)