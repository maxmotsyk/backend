from rest_framework import serializers
from .models import DeliveryMethod


class DeliveryMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryMethod
        fields = ['id', 'name', 'img', 'description', 'price']
