from django import forms
from .models import DevelopmentMilestone
from tinymce.widgets import TinyMCE


class DevelopmentMilestoneForm(forms.ModelForm):
    class Meta:
        model = DevelopmentMilestone
        fields = ['stage', 'week', 'start_age_months',
                  'end_age_months', 'description', 'image']
        widgets = {
            'description': TinyMCE(attrs={
                'cols': 80, 'rows': 10,
                'class': 'w-full border border-gray-300 rounded-lg py-2 px-4 shadow-sm focus:ring-2 focus:ring-sky-500 focus:border-sky-500'
            }),
            'stage': forms.Select(attrs={
                'class': 'rounded-lg shadow-sm border-gray-200 border py-2 px-4 w-full focus:ring-2 focus:ring-sky-500',
            }),
            'week': forms.Select(attrs={
                'class': 'rounded-lg shadow-sm border-gray-200 border py-2 px-4 w-full focus:ring-2 focus:ring-sky-500',
            }),
            'start_age_months': forms.NumberInput(attrs={
                'class': 'rounded-lg shadow-sm border-gray-200 border py-2 px-4 w-full focus:ring-2 focus:ring-sky-500',
            }),
            'end_age_months': forms.NumberInput(attrs={
                'class': 'rounded-lg shadow-sm border-gray-200 border py-2 px-4 w-full focus:ring-2 focus:ring-sky-500',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # get all weeks that are already in use
        used_weeks = DevelopmentMilestone.objects.filter(
            stage='prenatal').values_list('week', flat=True)

        # create a list of available weeks for prenatal stage
        available_weeks = [(i, f"Week {i}")
                           for i in range(1, 41) if i not in used_weeks]

        # if the week hasn't been used yet, add it to the available week. This prevents us from
        # duplicating milestones that already exist.
        if self.instance and self.instance.week and (self.instance.week, f"Week {self.instance.week}") not in available_weeks:
            available_weeks.append(
                (self.instance.week, f"Week {self.instance.week}"))

        # adjust field choices dynamically for prenatal stage
        self.fields['week'] = forms.ChoiceField(
            choices=[("", "Select a week")] + available_weeks,
            required=False,
            label="Development Week",
            widget=forms.Select(attrs={
                'class': 'rounded-lg shadow-sm border-gray-200 border py-2 px-4 w-full focus:ring-2 focus:ring-sky-500',
            }),
        )

        # dynamically set fields based on stage
        if self.instance and self.instance.stage == 'Prenatal':
            self.fields['week'].required = True
            self.fields['start_age_months'].required = False
            self.fields['end_age_months'].required = False
        elif self.instance and self.instance.stage == 'Postnatal':
            self.fields['week'].required = False
            self.fields['start_age_months'].required = True
            self.fields['end_age_months'].required = True


def clean(self):
    cleaned_data = super().clean()
    stage = cleaned_data.get('stage')
    week = cleaned_data.get('week')
    start_age_months = cleaned_data.get('start_age_months')
    end_age_months = cleaned_data.get('end_age_months')

    if week == "Select a week":
        week = None
        cleaned_data['week'] = None

    if stage == 'prenatal':
        if not week or not (1 <= int(week) <= 40):
            self.add_error(
                'week', "Week must be between 1 and 40 for prenatal milestones.")
        # clear postnatal fields
        cleaned_data['start_age_months'] = None
        cleaned_data['end_age_months'] = None

    elif stage == 'postnatal':
        # ensure week is cleared and ignored for postnatal milestones
        if week not in [None, '']:
            self.add_error(
                'week', "Week should not be set for postnatal milestones.")
        if start_age_months is None or end_age_months is None:
            self.add_error(
                'start_age_months', "Start and end age months must be set for postnatal milestones.")
            self.add_error(
                'end_age_months', "Start and end age months must be set for postnatal milestones.")
        elif start_age_months >= end_age_months:
            self.add_error('start_age_months',
                           "Start age must be less than end age.")

    return cleaned_data
