from rest_framework import serializers
from .models import DevelopmentMilestone
# serializer for development milestone
class DevelopmentMilestoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = DevelopmentMilestone
        fields = [
            'id',
            'stage',
            'week',
            'start_age_months',
            'end_age_months',
            'description',
            'image',
        ]
    
    # validation refactored from model save function
    def validate(self, data):
        stage = data.get('stage', 'prenatal')
        if stage == 'prenatal':
            week = data.get('week')
            if week is None or not (1 <= week <= 40):
                raise serializers.ValidationError({"week": "Week must be between 1 and 40 for prenatal milestones."})
            if data.get('start_age_months') is not None or data.get('end_age_months') is not None:
                raise serializers.ValidationError("Postnatal age fields should not be set for prenatal milestones.")
        elif stage == 'postnatal':
            if data.get('week') is not None:
                raise serializers.ValidationError({"week": "Week should not be set for postnatal milestones."})
            start_age = data.get('start_age_months')
            end_age = data.get('end_age_months')
            if start_age is None or end_age is None:
                raise serializers.ValidationError("Start and end age months must be set for postnatal milestones.")
            if start_age >= end_age:
                raise serializers.ValidationError("Start age must be less than end age.")
        return data