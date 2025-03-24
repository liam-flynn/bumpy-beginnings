from rest_framework import serializers
from .models import Article

# article serializer used for API
class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = [
            'id',
            'title',
            'subtitle',
            'text',
            'creation_date',
            'last_updated',
            'source',
            'related_week',
            'image',
        ]
        read_only_fields = ['id', 'creation_date', 'last_updated']