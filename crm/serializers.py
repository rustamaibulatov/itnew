from rest_framework import serializers

from .models import Car, Client

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = [
            'id',
            'full_name',
            'phone',
            'email',
            'created_at',
        ]
        read_only_fields = ['id', 'created_at']

class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = [
            'id',
            'client',
            'brand',
            'model',
            'year',
            'license_plate',
            'vin',
            'created_at',
        ]
        read_only_fields = ['id', 'created_at']
