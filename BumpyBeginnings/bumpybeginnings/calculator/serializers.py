from rest_framework import serializers
from .models import Benefit, BenefitRate, EligibilityCriteria

class BenefitSerializer(serializers.ModelSerializer):
    # any other benefit are classed as valid values for 'dependent_benefits'
    dependent_benefits = serializers.PrimaryKeyRelatedField(
        many=True, 
        queryset=Benefit.objects.all()
    )
    
    class Meta:
        model = Benefit
        fields = [
            'id',
            'name',
            'description',
            'frequency',
            'dependent_benefits',
        ]

class BenefitRateSerializer(serializers.ModelSerializer):
    # benefit needs to be a value found in the benefit table
    benefit = serializers.PrimaryKeyRelatedField(queryset=Benefit.objects.all())

    class Meta:
        model = BenefitRate
        fields = [
            'id',
            'benefit',
            'amount',
            'income_threshold_min',
            'income_threshold_max',
            'reduction_rate_per_unit',
            'income_unit',
            'effective_date',
        ]

class EligibilityCriteriaSerializer(serializers.ModelSerializer):
    # benefit needs to be a value found in the benefit table
    benefit = serializers.PrimaryKeyRelatedField(queryset=Benefit.objects.all())
    
    class Meta:
        model = EligibilityCriteria
        fields = [
            'id',
            'benefit',
            'criterion',
            'description',
            'value_type',
            'value',
            'match_type',
        ]