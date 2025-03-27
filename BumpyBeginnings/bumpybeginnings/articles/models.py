from django.db import models
from django.utils.timezone import now
from django_bleach.models import BleachField
from django.core.exceptions import ValidationError
import os


class Article(models.Model):
    title = models.CharField(max_length=255, blank=False, null=False)
    subtitle = models.CharField(max_length=255, blank=True, null=True)
    text = BleachField(
        allowed_tags=['a', 'ul', 'ol', 'li', 'strong', 'em', 'u', 'p', 'br', 'span'])
    creation_date = models.DateTimeField(default=now, editable=False)
    last_updated = models.DateTimeField(auto_now=True)
    source = models.URLField(max_length=500, blank=True, null=True)
    related_week = models.PositiveIntegerField(
        blank=True,
        null=True)
    image = models.ImageField(
        upload_to='article_images/', blank=True, null=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.title.strip():
            raise ValidationError(
                "The title cannot be blank or contain only whitespace.")
        if not self.text.strip():
            raise ValidationError(
                "The text content cannot be blank or contain only whitespace.")

        # check if there's an existing instance with this ID
        if self.pk:
            existing_article = Article.objects.filter(pk=self.pk).first()
            if existing_article and existing_article.image and existing_article.image != self.image:
                # delete the old image file
                if os.path.isfile(existing_article.image.path):
                    os.remove(existing_article.image.path)

        # save the new instance
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # delete the associated image file when deleting the article
        if self.image and os.path.isfile(self.image.path):
            os.remove(self.image.path)
        super().delete(*args, **kwargs)
