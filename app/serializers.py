from rest_framework import serializers
from .models import CompatibilityResult

class CompatibilityResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompatibilityResult
        fields = '__all__'
