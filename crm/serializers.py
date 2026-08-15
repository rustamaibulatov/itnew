from rest_framework import serializers

from .models import Car, Client, Repair, Part, Balance

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

class RepairSerializer(serializers.ModelSerializer):
    class Meta:
        model = Repair
        fields = [
            'id',
            'car',
            'description',
            'status',
            'work_cost',
            'created_at',
            'completed_at',
        ]
        read_only_fields = ['id', 'created_at']

class PartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Part
        fields = [
            'id',
            'repair',
            'name',
            'quantity',
            'unit_price',
        ]
        read_only_fields = ['id']

class BalanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Balance
        fields = [
            'id',
            'repair',
            'amount',
            'created_at',
        ]
        read_only_fields = ['id', 'created_at']
