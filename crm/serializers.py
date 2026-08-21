from rest_framework import serializers

from .models import Car, Client, Repair, Part, Balance, Mechanic, SparePart, RepairSparePart, Service, RepairService, RepairStatusHistory

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

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = [
            'id',
            'name',
            'price',
            'is_active',
            'created_at',
        ]
        read_only_fields = ['id', 'created_at']

class RepairServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = RepairService
        fields = [
            'id',
            'repair',
            'service',
            'price',
        ]
        read_only_fields = ['id', 'price']

    def create(self, validated_data):
        service = validated_data['service']
        repair = validated_data['repair']

        if repair.status == 'completed':
            raise serializers.ValidationError({
            'repair': 'Нельзя добавлять услуги в завершённый ремонт.'
        })
        validated_data['price'] = service.price
        return RepairService.objects.create(**validated_data)

    def update(self, instance, validated_data):
        if instance.repair.status == 'completed':
            raise serializers.ValidationError({
                'repair': 'Нельзя изменять услуги в завершённом ремонте.'
            })

        new_repair = validated_data.get('repair', instance.repair)
        new_service = validated_data.get('service', instance.service)

        if new_repair.id != instance.repair_id:
            raise serializers.ValidationError({
                'repair': 'Нельзя переносить услугу в другой ремонт.'
            })

        if new_service.id != instance.service_id:
            raise serializers.ValidationError({
                'service': 'Нельзя заменять услугу в этой записи. Удалите её и добавьте новую.'
            })

        return super().update(instance, validated_data)

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
        repair = validated_data['repair']

        if repair.status == 'completed':
            raise serializers.ValidationError({
                'repair': 'Нельзя добавлять запчасти в завершённый ремонт.'
            })

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

    def update(self, instance, validated_data):
        if instance.repair.status == 'completed':
            raise serializers.ValidationError({
                'repair': 'Нельзя изменять запчасти в завершённом ремонте.'
            })

        new_repair = validated_data.get('repair', instance.repair)
        new_spare_part = validated_data.get('spare_part', instance.spare_part)

        if new_repair.id != instance.repair_id:
            raise serializers.ValidationError({
                'repair': 'Нельзя переносить запчасть в другой ремонт.'
            })

        if new_spare_part.id != instance.spare_part_id:
            raise serializers.ValidationError({
                'spare_part': 'Нельзя заменить запчасть в этой записи. Удалите её и добавьте новую.'
            })

        old_quantity = instance.quantity
        new_quantity = validated_data.get('quantity', old_quantity)
        difference = new_quantity - old_quantity

        spare_part = instance.spare_part

        if difference > 0:
            if spare_part.stock_quantity < difference:
                raise serializers.ValidationError({
                    'quantity': 'Недостаточно запчастей на складе.'
                })

            spare_part.stock_quantity -= difference

        elif difference < 0:
            spare_part.stock_quantity += abs(difference)

        spare_part.save(update_fields=['stock_quantity'])

        return super().update(instance, validated_data)

class RepairStatusHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = RepairStatusHistory
        fields = [
            'status',
            'changed_at',
        ]

class RepairSerializer(serializers.ModelSerializer):
    services_total = serializers.SerializerMethodField()
    parts_total = serializers.SerializerMethodField()
    parts_cost = serializers.SerializerMethodField()
    total = serializers.SerializerMethodField()
    profit = serializers.SerializerMethodField()
    status_history = RepairStatusHistorySerializer(
    many=True,
    read_only=True,
)

    services = RepairServiceSerializer(
    source='repair_services',
    many=True,
    read_only=True,
)

    spare_parts = RepairSparePartSerializer(
    many=True,
    read_only=True,
)

    mechanic_details = MechanicSerializer(
    source='mechanic',
    read_only=True,
)

    car_details = CarSerializer(
    source='car',
    read_only=True,
)

    client_details = serializers.SerializerMethodField()

    class Meta:
        model = Repair
        fields = [
            'id',
            'car',
            'car_details',
            'client_details',
            'mechanic',
            'mechanic_details',
            'description',
            'status',
            'work_cost',
            'services',
            'spare_parts',
            'services_total',
            'parts_total',
            'parts_cost',
            'total',
            'profit',
            'created_at',
            'completed_at',
            'status_history',
        ]
        read_only_fields = ['id', 'created_at']
    def get_services_total(self, obj):
        return sum(
            item.price
            for item in obj.repair_services.all()
        )
    def get_parts_total(self, obj):
        return sum(
            item.sale_price * item.quantity
            for item in obj.spare_parts.all()
        )
    def get_parts_cost(self, obj):
        return sum(
            item.purchase_price * item.quantity
            for item in obj.spare_parts.all()
        )
    def get_total(self, obj):
        return (
            self.get_services_total(obj)
            + self.get_parts_total(obj)
        )
    def get_profit(self, obj):
        return (
            self.get_total(obj)
            - self.get_parts_cost(obj)
        )
    def create(self, validated_data):
        repair = Repair.objects.create(**validated_data)

        RepairStatusHistory.objects.create(
            repair=repair,
            status=repair.status,
    )

        return repair

    def update(self, instance, validated_data):
        if instance.status == 'completed':
            raise serializers.ValidationError({
                'repair': 'Завершённый ремонт нельзя изменять.'
            })

        old_status = instance.status
        new_status = validated_data.get('status', old_status)

        new_mechanic = validated_data.get('mechanic', instance.mechanic)

        if new_status == 'completed' and new_mechanic is None:
            raise serializers.ValidationError({
                'mechanic': 'Нельзя завершить ремонт без назначенного механика.'
            })

        allowed_transitions = {
            'new': ['in_progress'],
            'in_progress': ['completed'],
        }

        if new_status != old_status:
            allowed_statuses = allowed_transitions.get(old_status, [])

            if new_status not in allowed_statuses:
                raise serializers.ValidationError({
                    'status': f'Нельзя изменить статус с {old_status} на {new_status}.'
                })

        if old_status == 'completed' and new_status != 'completed':
            raise serializers.ValidationError({
                'status': 'Завершённый ремонт нельзя вернуть в работу.'
            })

        if new_status == 'completed' and old_status != 'completed':
            from django.utils import timezone
            validated_data['completed_at'] = timezone.now()

        elif new_status != 'completed':
            validated_data['completed_at'] = None

        updated_instance = super().update(instance, validated_data)

        if old_status != updated_instance.status:
            RepairStatusHistory.objects.create(
                repair=updated_instance,
                status=updated_instance.status,
            )

        return updated_instance

    def get_client_details(self, obj):
        if not obj.car or not obj.car.client:
            return None

        return ClientSerializer(obj.car.client).data

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
