from rest_framework import serializers

from .models import Car, Client, Repair, Part, Balance, Mechanic, SparePart, RepairSparePart

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

class MechanicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mechanic
        fields = [
            'id',
            'full_name',
            'phone',
            'specialization',
            'is_active',
            'created_at',
        ]
        read_only_fields = ['id', 'created_at']

class SparePartSerializer(serializers.ModelSerializer):
    class Meta:
        model = SparePart
        fields = [
            'id',
            'name',
            'article',
            'purchase_price',
            'sale_price',
            'stock_quantity',
            'is_active',
            'created_at',
        ]
        read_only_fields = ['id', 'created_at']

class RepairSparePartSerializer(serializers.ModelSerializer):
    class Meta:
        model = RepairSparePart
        fields = [
            'id',
            'repair',
            'spare_part',
            'quantity',
            'purchase_price',
            'sale_price',
        ]
        read_only_fields = ['id', 'purchase_price', 'sale_price']

    def create(self, validated_data):
        spare_part = validated_data['spare_part']
        quantity = validated_data['quantity']

        if spare_part.stock_quantity < quantity:
            raise serializers.ValidationError(
                {'quantity': 'Недостаточно запчастей на складе.'}
            )

        validated_data['purchase_price'] = spare_part.purchase_price
        validated_data['sale_price'] = spare_part.sale_price

        repair_spare_part = RepairSparePart.objects.create(**validated_data)

        spare_part.stock_quantity -= quantity
        spare_part.save(update_fields=['stock_quantity'])

        return repair_spare_part

class RepairSerializer(serializers.ModelSerializer):
    class Meta:
        model = Repair
        fields = [
            'id',
            'car',
            'mechanic',
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
