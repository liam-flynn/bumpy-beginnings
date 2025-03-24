from django import forms
from .models import Benefit, BenefitRate, EligibilityCriteria

class BenefitForm(forms.ModelForm):
    dependent_benefits = forms.ModelMultipleChoiceField(
        queryset=Benefit.objects.all(),
        required=False,
        widget=forms.SelectMultiple(attrs={
            'class': 'rounded-lg shadow-sm border border-gray-200 py-2 px-4 w-full focus:ring-2 focus:ring-sky-500',
        })
    )
    class Meta:
        model = Benefit
        fields = ['name', 'description', 'frequency', 'dependent_benefits']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'rounded-lg shadow-sm border border-gray-200 py-2 px-4 w-full focus:ring-2 focus:ring-sky-500',
                'placeholder': 'Enter Benefit Name'
            }),
            'description': forms.Textarea(attrs={
                'class': 'rounded-lg shadow-sm border border-gray-200 py-2 px-4 w-full focus:ring-2 focus:ring-sky-500',
                'placeholder': 'Enter a detailed description of the benefit'
            }),
            'frequency': forms.Select(attrs={
                'class': 'rounded-lg shadow-sm border border-gray-200 py-2 px-4 w-full focus:ring-2 focus:ring-sky-500'
            }),
        }


class BenefitRateForm(forms.ModelForm):
    class Meta:
        model = BenefitRate
        fields = [
            'benefit', 
            'amount', 
            'income_threshold_min', 
            'income_threshold_max', 
            'reduction_rate_per_unit', 
            'income_unit', 
            'effective_date'
        ]
        widgets = {
            'benefit': forms.Select(attrs={
                'class': 'rounded-lg shadow-sm border border-gray-200 py-2 px-4 w-full focus:ring-2 focus:ring-sky-500'
            }),
            'amount': forms.NumberInput(attrs={
                'class': 'rounded-lg shadow-sm border border-gray-200 py-2 px-4 w-full focus:ring-2 focus:ring-sky-500',
                'placeholder': 'Enter benefit amount'
            }),
            'income_threshold_min': forms.NumberInput(attrs={
                'class': 'rounded-lg shadow-sm border border-gray-200 py-2 px-4 w-full focus:ring-2 focus:ring-sky-500',
                'placeholder': 'Enter minimum income threshold (e.g., 60000)'
            }),
            'income_threshold_max': forms.NumberInput(attrs={
                'class': 'rounded-lg shadow-sm border border-gray-200 py-2 px-4 w-full focus:ring-2 focus:ring-sky-500',
                'placeholder': 'Enter maximum income threshold (e.g., 80000)'
            }),
            'reduction_rate_per_unit': forms.NumberInput(attrs={
                'class': 'rounded-lg shadow-sm border border-gray-200 py-2 px-4 w-full focus:ring-2 focus:ring-sky-500',
                'placeholder': 'Enter reduction percentage per income unit (e.g., 1 for 1%)'
            }),
            'income_unit': forms.NumberInput(attrs={
                'class': 'rounded-lg shadow-sm border border-gray-200 py-2 px-4 w-full focus:ring-2 focus:ring-sky-500',
                'placeholder': 'Enter income unit (e.g., 200 for every £200)'
            }),
            'effective_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'rounded-lg shadow-sm border border-gray-200 py-2 px-4 w-full focus:ring-2 focus:ring-sky-500'
            }),
        }


class EligibilityCriteriaForm(forms.ModelForm):
    class Meta:
        model = EligibilityCriteria
        fields = ['benefit', 'criterion', 'description', 'value_type', 'value', 'match_type']
        widgets = {
            'benefit': forms.Select(attrs={
                'class': 'rounded-lg shadow-sm border border-gray-200 py-2 px-4 w-full focus:ring-2 focus:ring-sky-500'
            }),
            'criterion': forms.TextInput(attrs={
                'class': 'rounded-lg shadow-sm border border-gray-200 py-2 px-4 w-full focus:ring-2 focus:ring-sky-500',
                'placeholder': 'Enter criterion name (e.g., Income, Residency)'
            }),
            'description': forms.Textarea(attrs={
                'class': 'rounded-lg shadow-sm border border-gray-200 py-2 px-4 w-full focus:ring-2 focus:ring-sky-500',
                'placeholder': 'Provide a detailed explanation of this criterion'
            }),
            'value_type': forms.Select(attrs={
                'class': 'rounded-lg shadow-sm border border-gray-200 py-2 px-4 w-full focus:ring-2 focus:ring-sky-500'
            }),
            'value': forms.TextInput(attrs={
                'class': 'rounded-lg shadow-sm border border-gray-200 py-2 px-4 w-full focus:ring-2 focus:ring-sky-500',
                'placeholder': 'Enter the required value or condition'
            }),
            'match_type': forms.Select(attrs={
                'class': 'rounded-lg shadow-sm border border-gray-200 py-2 px-4 w-full focus:ring-2 focus:ring-sky-500'
            }),
        }
    def __init__(self, *args, **kwargs):
        super(EligibilityCriteriaForm, self).__init__(*args, **kwargs)
        # start with the no match type i.e. exact match, higher than, lower than, etc
        match_type = None
        # if editing an criteria, make sure to get the current match type, otherwise use the initial value
        if self.data:
            match_type = self.data.get('match_type')
        elif 'match_type' in self.initial:
            match_type = self.initial.get('match_type')
        # if the the match type is 'none' we don't force the user to provide a 'value'
        if match_type == 'none':
            self.fields['value'].required = False
        else:
            self.fields['value'].required = True