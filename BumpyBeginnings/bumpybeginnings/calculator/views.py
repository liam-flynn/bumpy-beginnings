from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from .forms import BenefitForm, BenefitRateForm, EligibilityCriteriaForm
from .models import Benefit, EligibilityCriteria, BenefitRate
from django.contrib import messages
import math
from bumpybeginnings.breadcrumbs import get_breadcrumbs
from django.contrib.auth.decorators import login_required

# only staff members should be able to access the create benefit page


@user_passes_test(lambda user: user.is_staff, login_url='/')
def create_benefit(request):
    if request.method == "POST":
        form = BenefitForm(request.POST)
        # if form is valid, save benefit and inform user.
        if form.is_valid():
            form.save()
            messages.success(request, "Benefit successfully created")
            return redirect("benefit_list")
        # if errors on the form, inform user via message
        else:
            messages.error(
                request, "There were errors in the Benefit form. Please correct them and try again.")
    else:
        form = BenefitForm()
    return render(request, "create_benefit.html", {"benefit_form": form})


@user_passes_test(lambda user: user.is_staff, login_url='/')
def edit_benefit(request, benefit_id):
    # collect the data for the existing benefit
    benefit = get_object_or_404(Benefit, id=benefit_id)
    if request.method == 'POST':
        # use the returned data to populate the form
        form = BenefitForm(request.POST, instance=benefit)
        # save on valid form, report error on invalid form
        if form.is_valid():
            form.save()
            messages.success(request, "Benefit successfully amended")
            return redirect('benefit_list')
        else:
            messages.error(
                request, "There were errors in the Benefit form. Please correct them and try again.")
    else:
        form = BenefitForm(instance=benefit)
    return render(request, 'edit_benefit.html', {'form': form, 'benefit': benefit})


@user_passes_test(lambda user: user.is_staff, login_url='/')
def delete_benefit(request, benefit_id):
    benefit = get_object_or_404(Benefit, id=benefit_id)
    benefit.delete()
    messages.success(request, "Benefit successfully deleted.")
    return redirect('benefit_list')


@user_passes_test(lambda user: user.is_staff, login_url='/')
def create_benefit_rate(request):
    if request.method == "POST":
        form = BenefitRateForm(request.POST)
        # save benefit rate on valid form, report error on invalid form
        if form.is_valid():
            form.save()
            messages.success(request, "New Benefit rate successfully created")
            return redirect("benefit_list")
        else:
            messages.error(
                request, "There were errors in the Benefit Rate form. Please correct them and try again.")
    else:
        form = BenefitRateForm()
    return render(request, "create_benefit_rate.html", {"rate_form": form})


@user_passes_test(lambda user: user.is_staff, login_url='/')
def edit_benefit_rate(request, rate_id):
    # collect the data for the existing benefit rate
    rate = get_object_or_404(BenefitRate, id=rate_id)
    if request.method == 'POST':
        form = BenefitRateForm(request.POST, instance=rate)
        # save on valid form, report error on invalid form
        if form.is_valid():
            form.save()
            messages.success(request, "Benefit rate successfully amended")
            return redirect('benefit_list')
        else:
            messages.error(
                request, "There were errors in the Benefit Rate form. Please correct them and try again.")
    else:
        form = BenefitRateForm(instance=rate)
    return render(request, 'edit_benefit_rate.html', {'form': form, 'rate': rate})


@user_passes_test(lambda user: user.is_staff, login_url='/login/')
def delete_benefit_rate(request, rate_id):
    rate = get_object_or_404(BenefitRate, id=rate_id)
    rate.delete()
    messages.success(request, "Benefit Rate successfully deleted.")
    return redirect('benefit_list')


@user_passes_test(lambda user: user.is_staff, login_url='/')
def create_eligibility_criteria(request):
    if request.method == "POST":
        form = EligibilityCriteriaForm(request.POST)
        # save eligibility criteria rate on valid form, report error on invalid form
        if form.is_valid():
            form.save()
            messages.success(request, "New Criteria successfully created")
            return redirect("benefit_list")
        else:
            messages.error(
                request, "There were errors in the Eligibility Criteria form. Please correct them and try again.")
    else:
        form = EligibilityCriteriaForm()
    return render(request, "create_eligibility_criteria.html", {"criteria_form": form})


@user_passes_test(lambda user: user.is_staff, login_url='/')
def edit_eligibility_criteria(request, criteria_id):
    # collect the data for the existing eligibility criteria
    criteria = get_object_or_404(EligibilityCriteria, id=criteria_id)
    if request.method == 'POST':
        form = EligibilityCriteriaForm(request.POST, instance=criteria)
        # save on valid form, report error on invalid form
        if form.is_valid():
            form.save()
            messages.success(request, "Criteria successfully amended")
            return redirect('benefit_list')
        else:
            messages.error(
                request, "There were errors in the Eligibility Criteria form. Please correct them and try again.")
    else:
        form = EligibilityCriteriaForm(instance=criteria)
    return render(request, 'edit_eligibility_criteria.html', {'form': form, 'criteria': criteria})


@user_passes_test(lambda user: user.is_staff, login_url='/')
def delete_eligibility_criteria(request, criteria_id):
    criteria = get_object_or_404(EligibilityCriteria, id=criteria_id)
    criteria.delete()
    messages.success(request, "Eligibility Criteria successfully deleted.")
    return redirect('benefit_list')


@user_passes_test(lambda user: user.is_staff, login_url='/')
def manage_benefits_list(request):
    # collect all instances of benefits, rates and criteria and pass to view
    benefits = Benefit.objects.all().order_by('name')
    rates = BenefitRate.objects.all().order_by('benefit__name')
    criteria = EligibilityCriteria.objects.all().order_by('benefit__name')
    context = {
        'benefits': benefits,
        'rates': rates,
        'criteria': criteria,
        "breadcrumbs": get_breadcrumbs(request)
    }
    return render(request, 'manage_benefits.html', context)


@login_required(login_url='/login')
def questionnaire(request):
    if request.method == "POST":
        applicant_answers = request.POST

        # first, check the universal residency question.
        residency = applicant_answers.get('residency')
        if residency is None or residency.lower() != "true":
            # if the applicant doesn't live in the UK, show no eligible benefits.
            return render(request, "questionnaire_results.html", {
                "eligible_benefits": [],
                "calculated_benefits": [],
                "salary": None,
                "error_message": "Unfortunately, you must live in the UK to qualify for any benefits."
            })

        # get the salary (asked in the hard-coded question)
        salary_raw = applicant_answers.get('salary')
        # if you can't convert it to a float, use 0.0.
        try:
            salary = float(salary_raw)
        except (TypeError, ValueError):
            salary = 0.0

        eligible_benefits = []
        calculated_benefits = []

        # get all benefits with their criteria and rates
        # help from https://johnnymetz.com/posts/five-ways-to-get-django-objects-with-a-related-object/
        benefits = Benefit.objects.prefetch_related(
            "eligibility_criteria", "rates").all()

        # loop through each benefit, checking if its criteria has been met
        for benefit in benefits:
            criteria = benefit.eligibility_criteria.all()
            meets_all_criteria = True

            for criterion in criteria:
                # use a unique field name for each criterion
                field_name = f"criterion_{criterion.id}"
                # for criteria involving income, use the salary input
                if "income" in criterion.criterion.lower():
                    answer = salary_raw
                else:
                    answer = applicant_answers.get(field_name)

                # if the criterin is a boolean
                if criterion.value_type == "boolean":
                    answer_bool = answer.lower() == "true" if answer else False
                    criterion_value_bool = (
                        criterion.value.lower() == "true") if criterion.value else False
                    if criterion.match_type == "exact" and answer_bool != criterion_value_bool:
                        meets_all_criteria = False
                        break

                # if the criterion is numeric
                elif criterion.value_type == "numeric":
                    # handle if user provides invalid input
                    try:
                        answer_numeric = float(answer)
                        criterion_numeric = float(criterion.value)
                    except (ValueError, TypeError):
                        meets_all_criteria = False
                        break

                    if criterion.match_type == "exact" and answer_numeric != criterion_numeric:
                        meets_all_criteria = False
                        break
                    elif criterion.match_type == "gt" and answer_numeric <= criterion_numeric:
                        meets_all_criteria = False
                        break
                    elif criterion.match_type == "lt" and answer_numeric >= criterion_numeric:
                        meets_all_criteria = False
                        break

                # if the criterion is text based
                elif criterion.value_type == "text":
                    if criterion.match_type == "exact":
                        if answer.strip().lower() != criterion.value.strip().lower():
                            meets_all_criteria = False
                            break

            if meets_all_criteria:
                eligible_benefits.append(benefit)
                # for simplicity, assume one rate per benefit.
                rate = benefit.rates.first()
                if rate:
                    if rate.income_threshold_min is not None and salary > float(rate.income_threshold_min):
                        # calculate the reduction unit. For every £200 above £50,000 benefit is reduced by x%
                        reduction_unit = round(
                            float(
                                rate.amount) * (1 - (1 - (float(rate.reduction_rate_per_unit) / 100.0))),
                            3
                        )
                        # calculate by how many income units the user's salary exceeds the the minimum threshold
                        units = math.floor(
                            (salary - float(rate.income_threshold_min)) / float(rate.income_unit))
                        # finally calculate the amount
                        calculated_amount = max(
                            0, float(rate.amount) - (reduction_unit * units))
                    # if the benefit is not affected by a reduction,  just pass it back
                    else:
                        calculated_amount = float(rate.amount)
                else:
                    calculated_amount = None
                calculated_benefits.append({
                    'benefit': benefit,
                    'calculated_amount': calculated_amount
                })

        return render(request, "questionnaire_results.html", {
            "eligible_benefits": eligible_benefits,
            "calculated_benefits": calculated_benefits,
            "salary": salary,
            "breadcrumbs": get_breadcrumbs(request)
        })
    else:
        # exclude income-based criteria, handled by salary question
        criterias = EligibilityCriteria.objects.exclude(
            criterion__icontains="income"
        )
        # group criteria by the criterion field (i.e "Residency", "Disability", "Child Age")
        grouped_criteria = {}
        for criteria in criterias:
            group = criteria.criterion
            grouped_criteria.setdefault(group, []).append(criteria)

        return render(request, "questionnaire.html", {"grouped_criteria": grouped_criteria, "breadcrumbs": get_breadcrumbs(request)})
