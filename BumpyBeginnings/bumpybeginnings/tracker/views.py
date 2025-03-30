from datetime import timedelta
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test,  login_required
from .forms import DevelopmentMilestoneForm
from .models import DevelopmentMilestone
from users.models import SiteUser
from django.utils.timezone import now
from django.views.generic import ListView
from bumpybeginnings.breadcrumbs import get_breadcrumbs
from django.contrib.auth.mixins import LoginRequiredMixin


# get a list of all milestones
class DevelopmentMilstoneListView(LoginRequiredMixin, ListView):
    model = DevelopmentMilestone
    template_name = 'milestones.html'
    login_url = '/login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['breadcrumbs'] = get_breadcrumbs(self.request)
        return context

    def get_queryset(self):
        return DevelopmentMilestone.objects.all().order_by('week', 'start_age_months')

# only staff members allowed to create new milestones


@user_passes_test(lambda user: user.is_staff, login_url='/login/')
def create_milestone(request):
    if request.method == 'POST':
        form = DevelopmentMilestoneForm(request.POST,  request.FILES)
        if form.is_valid():
            form.save()
            return redirect('trackers')
        else:
            print(form.errors)
    else:
        form = DevelopmentMilestoneForm()

    return render(request, 'create_milestone.html', {'form': form, 'breadcrumbs': get_breadcrumbs(request)})


@user_passes_test(lambda user: user.is_staff, login_url='/login/')
def delete_milestone(request, id):
    # get the milestone using the milestone id
    milestone = get_object_or_404(DevelopmentMilestone, id=id)
    # delete and redirect back to the page
    milestone.delete()
    return redirect('trackers')


@user_passes_test(lambda user: user.is_staff, login_url='/login/')
def edit_milestone(request, id):
    # get the milestone using the milestone id
    milestone = get_object_or_404(DevelopmentMilestone, id=id)
    if request.method == 'POST':
        # pass the data to the form to populate the fields
        form = DevelopmentMilestoneForm(
            request.POST, request.FILES, instance=milestone)
        if form.is_valid():
            form.save()
            return redirect('trackers')
    else:
        form = DevelopmentMilestoneForm(instance=milestone)

    return render(request, 'edit_milestone.html', {'form': form, 'milestone': milestone, 'breadcrumbs': get_breadcrumbs(request)})


def view_milestone(request, id):
    milestone = get_object_or_404(DevelopmentMilestone, id=id)
    context = {
        'milestone': milestone,
        'breadcrumbs': get_breadcrumbs(request)
    }
    return render(request, 'view_milestone.html', context)


def get_current_milestone(request):
    # fetch the SiteUser
    site_user = get_object_or_404(SiteUser, user=request.user)

    # calculate today's date
    today = now().date()

    # calculate conception and due dates
    conception_date = site_user.dueDate - timedelta(weeks=40)
    pregnancy_week = max((today - conception_date).days // 7, 0)

    # determine if the user is prenatal or postnatal
    if today < site_user.dueDate:
        # prenatal stage: Calculate weeks of pregnancy
        milestones = DevelopmentMilestone.objects.filter(
            stage='prenatal', week__lte=pregnancy_week).order_by('-week')
    else:
        # postnatal stage: calculate baby's age in months
        # Approximate months
        baby_age_months = ((today - site_user.dueDate).days // 30)
        milestones = DevelopmentMilestone.objects.filter(
            stage='postnatal', start_age_months__lte=baby_age_months).order_by('-start_age_months')

    return render(request, 'milestone.html', {'milestone': milestones.first()})
