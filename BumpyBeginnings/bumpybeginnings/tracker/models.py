from django.db import models
from django.core.exceptions import ValidationError
from django_bleach.models import BleachField
import os


class DevelopmentMilestone(models.Model):
    STAGE_CHOICES = [
        ('prenatal', 'Prenatal'),
        ('postnatal', 'Postnatal'),
    ]

    stage = models.CharField(
        max_length=10,
        choices=STAGE_CHOICES,
        default='prenatal',
    )

    week = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="Applicable for prenatal milestones (1-40 weeks).",
    )
    start_age_months = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="Start age in months for postnatal milestones.",
    )
    end_age_months = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="End age in months for postnatal milestones.",
    )
    description = BleachField(
        allowed_tags=['a', 'ul', 'ol', 'li', 'strong', 'em', 'u', 'p', 'br', 'span'])
    image = models.ImageField(
        upload_to='milestone_images/',
        null=True,
        blank=True,
    )

    def clean(self):
        if self.stage == 'prenatal':
            if self.week is None or not (1 <= self.week <= 40):
                raise ValidationError(
                    "Week must be between 1 and 40 for prenatal milestones.")
            if self.start_age_months is not None or self.end_age_months is not None:
                raise ValidationError(
                    "Postnatal age fields should not be set for prenatal milestones.")
        elif self.stage == 'postnatal':
            self.week = None
            if self.week is not None:
                raise ValidationError(
                    "Week should not be set for postnatal milestones.")
            if self.start_age_months is None or self.end_age_months is None:
                raise ValidationError(
                    "Start and end age months must be set for postnatal milestones.")
            if self.start_age_months >= self.end_age_months:
                raise ValidationError("Start age must be less than end age.")

    def __str__(self):
        if self.stage == 'prenatal':
            return f"Prenatal Week {self.week}: {self.description[:50]}"
        else:
            return f"Postnatal {self.start_age_months}-{self.end_age_months} Months: {self.description[:50]}"

    def save(self, *args, **kwargs):
        # check if there's an existing instance with this ID
        if self.pk:
            existing_milestone = DevelopmentMilestone.objects.filter(
                pk=self.pk).first()
            if existing_milestone and existing_milestone.image and existing_milestone.image != self.image:
                # delete the old image file
                if os.path.isfile(existing_milestone.image.path):
                    os.remove(existing_milestone.image.path)

        # save the new instance
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # delete the linked image file when deleting the milestone
        if self.image and os.path.isfile(self.image.path):
            os.remove(self.image.path)
        super().delete(*args, **kwargs)
