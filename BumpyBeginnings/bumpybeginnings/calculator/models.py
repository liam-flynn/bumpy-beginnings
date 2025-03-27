from django.db import models
from django.utils.timezone import now


class Benefit(models.Model):
    name = models.CharField(max_length=255, unique=True,
                            null=False, blank=False)
    description = models.TextField(null=False, blank=False)
    frequency = models.CharField(
        max_length=20,
        choices=[("once", "Once"), ("weekly", "Weekly"),
                 ("monthly", "Monthly"), ("annually", "Annually")],
        default="monthly",
    )
    # being successful for one benefit can automatically qualify you for another.
    dependent_benefits = models.ManyToManyField(
        'self', blank=True, symmetrical=False, related_name='prerequisite_for')

    def __str__(self):
        return self.name


class BenefitRate(models.Model):
    benefit = models.ForeignKey(
        Benefit, on_delete=models.CASCADE, related_name="rates")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    # these new fields define the income thresholds and reduction settings for the benefit.
    income_threshold_min = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True,
    )
    income_threshold_max = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True,
    )
    reduction_rate_per_unit = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True,
    )
    income_unit = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True,
    )
    effective_date = models.DateField(default=now)

    def __str__(self):
        return f"{self.benefit.name} Rate: {self.amount} effective {self.effective_date}"


class EligibilityCriteria(models.Model):

    MATCH_TYPE_CHOICES = [
        ("exact", "Exact match"),
        ("gt", "Greater than"),
        ("lt", "Less than"),
        ("none", "No comparison"),
    ]

    benefit = models.ForeignKey(
        Benefit, on_delete=models.CASCADE, related_name="eligibility_criteria")
    criterion = models.CharField(max_length=255)
    description = models.TextField(null=False, blank=False)
    value_type = models.CharField(
        max_length=20,
        choices=[("boolean", "Boolean"),
                 ("numeric", "Numeric"), ("text", "Text")],
    )
    value = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        default=None
    )
    match_type = models.CharField(
        max_length=10,
        choices=MATCH_TYPE_CHOICES,
        default="exact",
    )

    def __str__(self):
        return f"{self.criterion} for {self.benefit.name}"
