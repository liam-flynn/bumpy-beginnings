import string
from django.urls import reverse
from hypothesis import given, assume, settings, HealthCheck
import hypothesis.strategies as st
from hypothesis.extra.django import TestCase as HypothesisTestCase
from calculator.models import Benefit
from decimal import Decimal
from .strategies import benefit_name_strategy, benefit_description_strategy, frequency_strategy, create_staff_user, criterion_strategy, criteria_description_strategy,value_type_strategy,match_type_strategy, decimal_strategy,reduction_rate_strategy, effective_date_value

class BenefitViewTests(HypothesisTestCase):

    # test create_benefit view.
    @settings(deadline=1000, suppress_health_check=[HealthCheck.filter_too_much])
    @given(
        name=benefit_name_strategy,
        description=benefit_description_strategy,
        frequency=frequency_strategy
    )
    def test_create_benefit_view(self, name, description, frequency):
        # create a staff member and login (only staff can CUD benefits)
        staff = create_staff_user("benefit_creator")
        self.client.login(username="benefit_creator", password="password")
        # create the POST data
        data = {
            'name': name,
            'description': description,
            'frequency': frequency,
            'dependent_benefits': []
        }
        # attempt to create benefit. check that you are redirected (302) upon success
        response = self.client.post(reverse("create_benefit"), data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Benefit.objects.filter(name=name.strip()).exists())

    # test "edit_benefit" view.
    @settings(deadline=1000, suppress_health_check=[HealthCheck.filter_too_much])
    @given(
        # select random replacement values (not null) to replace current values
        new_name=st.text(min_size=1, max_size=100, alphabet=string.printable)
                 .filter(lambda s: s.strip() != ""),

        new_description=st.text(min_size=1, max_size=500, alphabet=string.printable)
                          .filter(lambda s: s.strip() != ""),

        new_frequency=st.sampled_from(["once", "weekly", "monthly", "annually"])
    )
    def test_edit_benefit_view(self, new_name, new_description, new_frequency):
        staff = create_staff_user("benefit_editor", "password")
        self.client.login(username="benefit_editor", password="password")
        # create an initial benefit.
        benefit = Benefit.objects.create(
            name="Initial Benefit",
            description="Initial description",
            frequency="monthly"
        )
        # get the url of the view and pass the id of the benefit we have just created.
        url = reverse("edit_benefit", kwargs={'benefit_id': benefit.id})
        # POST data with the info we are going to update.
        data = {
            'name': new_name,
            'description': new_description,
            'frequency': new_frequency,
            'dependent_benefits': []
        }
        response = self.client.post(url, data)
        # the view should redirect on success.
        self.assertEqual(response.status_code, 302)
        benefit.refresh_from_db()

        # since the form cleans input by stripping whitespace, compare with stripped values.
        self.assertEqual(benefit.name, new_name.strip())
        self.assertEqual(benefit.description, new_description.strip())
        self.assertEqual(benefit.frequency, new_frequency)

    # test "delete_benefit" view.
    def test_delete_benefit_view(self):
        staff = create_staff_user("benefit_deleter")
        self.client.login(username="benefit_deleter", password="password")
        benefit = Benefit.objects.create(
            name="Delete Benefit",
            description="To be deleted",
            frequency="monthly"
        )
        url = reverse("delete_benefit", kwargs={'benefit_id': benefit.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        with self.assertRaises(Benefit.DoesNotExist):
            Benefit.objects.get(id=benefit.id)

    # test create_benefit_rate view.
    @settings(deadline=1000, suppress_health_check=[HealthCheck.filter_too_much])
    # uses various strategies as specific format of data required for each field
    @given(
        amount=decimal_strategy,
        income_threshold_min=decimal_strategy,
        income_threshold_max=decimal_strategy,
        reduction_rate_per_unit=reduction_rate_strategy,
        income_unit=decimal_strategy
    )
    def test_create_benefit_rate_view(self, amount, income_threshold_min, income_threshold_max, reduction_rate_per_unit, income_unit):
        # ensure thresholds make sense.
        assume(income_threshold_min <= income_threshold_max)
        staff = create_staff_user("rate_creator")
        self.client.login(username="rate_creator", password="password")
        # create a Benefit to attach the rate.
        benefit = Benefit.objects.create(
            name="Rate Benefit",
            description="Benefit for rate test",
            frequency="monthly"
        )
        data = {
            'benefit': benefit.id,
            'amount': f"{amount:.2f}",
            'income_threshold_min': f"{income_threshold_min:.2f}",
            'income_threshold_max': f"{income_threshold_max:.2f}",
            'reduction_rate_per_unit': f"{reduction_rate_per_unit:.2f}",
            'income_unit': f"{income_unit:.2f}",
            'effective_date': effective_date_value
        }
        response = self.client.post(reverse("create_benefit_rate"), data)
        self.assertEqual(response.status_code, 302)
        # verify that a rate was created for the given benefit.
        self.assertTrue(benefit.rates.filter(amount=f"{amount:.2f}").exists())

    # test "edit_benefit_rate" view.
    @settings(deadline=1000, suppress_health_check=[HealthCheck.filter_too_much])
    @given(
        new_amount=st.floats(min_value=0.01, max_value=1000, allow_nan=False, allow_infinity=False),
        new_income_threshold_min=st.floats(min_value=0.01, max_value=1000, allow_nan=False, allow_infinity=False),
        new_income_threshold_max=st.floats(min_value=0.01, max_value=1000, allow_nan=False, allow_infinity=False),
        new_reduction_rate_per_unit=st.floats(min_value=0.01, max_value=100, allow_nan=False, allow_infinity=False),
        new_income_unit=st.floats(min_value=0.01, max_value=1000, allow_nan=False, allow_infinity=False)
    )
    def test_edit_benefit_rate_view(self, new_amount, new_income_threshold_min, new_income_threshold_max, new_reduction_rate_per_unit, new_income_unit):
        # ensure that income_threshold_min is not greater than income_threshold_max.
        assume(new_income_threshold_min <= new_income_threshold_max)
        
        staff = create_staff_user("rate_editor")
        self.client.login(username="rate_editor", password="password")
        # create a Benefit to attach the rate.
        benefit = Benefit.objects.create(
            name="Benefit for editing rate",
            description="Benefit for editing rate",
            frequency="monthly"
        )
        # create an initial rate.
        rate = benefit.rates.create(
            amount="100.00",
            income_threshold_min="50.00",
            income_threshold_max="200.00",
            reduction_rate_per_unit="5.00",
            income_unit="10.00",
            effective_date=effective_date_value
        )
        url = reverse("edit_benefit_rate", kwargs={'rate_id': rate.id})
        data = {
            'benefit': benefit.id,
            'amount': f"{new_amount:.2f}",
            'income_threshold_min': f"{new_income_threshold_min:.2f}",
            'income_threshold_max': f"{new_income_threshold_max:.2f}",
            'reduction_rate_per_unit': f"{new_reduction_rate_per_unit:.2f}",
            'income_unit': f"{new_income_unit:.2f}",
            'effective_date': effective_date_value
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        rate.refresh_from_db()
        # convert the expected value to "Decimal" for a proper comparison.
        self.assertEqual(rate.amount, Decimal(f"{new_amount:.2f}"))

    # test "delete_benefit_rate" view.
    def test_delete_benefit_rate_view(self):
        staff = create_staff_user("rate_deleter")
        self.client.login(username="rate_deleter", password="password")
        benefit = Benefit.objects.create(
            name="Benefit for deleting rate",
            description="Benefit for deleting rate",
            frequency="monthly"
        )
        rate = benefit.rates.create(
            amount="100.00",
            income_threshold_min="50.00",
            income_threshold_max="200.00",
            reduction_rate_per_unit="5.00",
            income_unit="10.00",
            effective_date=effective_date_value
        )
        url = reverse("delete_benefit_rate", kwargs={'rate_id': rate.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        # assert that the BenefitRate no longer exists in the database
        self.assertFalse(rate.__class__.objects.filter(id=rate.id).exists())


    # test "create_eligibility_criteria" view.
    @settings(deadline=1000, suppress_health_check=[HealthCheck.filter_too_much])
    @given(
        criterion=criterion_strategy,
        description=criteria_description_strategy,
        value_type=value_type_strategy,
        match_type=match_type_strategy
    )
    def test_create_eligibility_criteria_view(self, criterion, description, value_type, match_type):
        staff = create_staff_user("criteria_creator")
        self.client.login(username="criteria_creator", password="password")
        # create a Benefit to associate with this criteria.
        benefit = Benefit.objects.create(
            name="Criteria Benefit",
            description="For eligibility criteria test",
            frequency="monthly"
        )
        # determine a value based on match_type.
        value = "" if match_type == "none" else "Value"
        data = {
            'benefit': benefit.id,
            'criterion': criterion,
            'description': description,
            'value_type': value_type,
            'value': value,
            'match_type': match_type
        }
        # pass the data to the view and check for redirect on success and criteria created
        response = self.client.post(reverse("create_eligibility_criteria"), data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(benefit.eligibility_criteria.filter(criterion=criterion.strip()).exists())

    # test "edit_eligibility_criteria" view.
    @settings(deadline=1000, suppress_health_check=[HealthCheck.filter_too_much])
    # create new values used to replace the old
    @given(
        new_criterion=criterion_strategy,
        new_description=criteria_description_strategy,
        new_value_type=value_type_strategy,
        new_match_type=match_type_strategy
    )
    def test_edit_eligibility_criteria_view(self, new_criterion, new_description, new_value_type, new_match_type):
        staff = create_staff_user("criteria_editor")
        self.client.login(username="criteria_editor", password="password")
        benefit = Benefit.objects.create(
            name="Benefit for editing criteria",
            description="Benefit for editing criteria",
            frequency="monthly"
        )
        # create an initial "EligibilityCriteria".
        criteria = benefit.eligibility_criteria.create(
            criterion="Initial Criterion",
            description="Initial description",
            value_type="text",
            value="Initial Value",
            match_type="exact"
        )
        url = reverse("edit_eligibility_criteria", kwargs={'criteria_id': criteria.id})
        new_value = "" if new_match_type == "none" else "NewValue"
        data = {
            'benefit': benefit.id,
            'criterion': new_criterion,
            'description': new_description,
            'value_type': new_value_type,
            'value': new_value,
            'match_type': new_match_type
        }
        response = self.client.post(url, data)
        # pass the data to the view and check for redirect on success and criteria altered
        self.assertEqual(response.status_code, 302)
        criteria.refresh_from_db()
        self.assertEqual(criteria.criterion, new_criterion.strip())

    # test "delete_eligibility_criteria" view.
    def test_delete_eligibility_criteria_view(self):
        staff = create_staff_user("criteria_deleter")
        self.client.login(username="criteria_deleter", password="password")
        benefit = Benefit.objects.create(
            name="Benefit for deleting criteria",
            description="Benefit for deleting criteria",
            frequency="monthly"
        )
        criteria = benefit.eligibility_criteria.create(
            criterion="Delete Criterion",
            description="Delete description",
            value_type="text",
            value="Value",
            match_type="exact"
        )
        url = reverse("delete_eligibility_criteria", kwargs={'criteria_id': criteria.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        with self.assertRaises(criteria.__class__.DoesNotExist):
            criteria.__class__.objects.get(id=criteria.id)

    # test "manage_benefits_list" view.
    def test_manage_benefits_list_view(self):
        staff = create_staff_user("benefits_manager")
        self.client.login(username="benefits_manager", password="password")
        # create some benefits, rates, and criteria.
        benefit1 = Benefit.objects.create(
            name="Benefit One",
            description="Desc One",
            frequency="monthly"
        )
        benefit2 = Benefit.objects.create(
            name="Benefit Two",
            description="Desc Two",
            frequency="weekly"
        )
        benefit1.rates.create(
            amount="100.00",
            income_threshold_min="50.00",
            income_threshold_max="200.00",
            reduction_rate_per_unit="5.00",
            income_unit="10.00",
            effective_date=effective_date_value
        )
        benefit2.eligibility_criteria.create(
            criterion="Criterion Two",
            description="Criterion Desc",
            value_type="boolean",
            value="true",
            match_type="exact"
        )
        response = self.client.get(reverse("benefit_list"))
        self.assertEqual(response.status_code, 200)
        self.assertIn("benefits", response.context)
        self.assertIn("rates", response.context)
        self.assertIn("criteria", response.context)