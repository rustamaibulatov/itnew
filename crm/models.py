from django.db import models

class Client(models.Model):
    full_name = models.CharField(max_length=150)
    phone = models.CharField(max_length=20, unique=True)
    email = models.EmailField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name

class Car(models.Model):
    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name='cars',
    )
    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.PositiveSmallIntegerField()
    license_plate = models.CharField(max_length=20, unique=True)
    vin = models.CharField(max_length=17, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.brand} {self.model} — {self.license_plate}'

class Mechanic(models.Model):
    full_name = models.CharField(max_length=150)
    phone = models.CharField(max_length=20, blank=True)
    specialization = models.CharField(max_length=150, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name

class Repair(models.Model):
    car = models.ForeignKey(
        Car,
        on_delete=models.CASCADE,
        related_name='repairs',
)
    mechanic = models.ForeignKey(
        Mechanic,
        on_delete=models.SET_NULL,
        related_name='repairs',
        null=True,
        blank=True,
)
    description = models.TextField()
    STATUS_CHOICES = [
        ('new', 'Новый'),
        ('in_progress', 'В работе'),
        ('waiting_parts', 'Ждёт запчасти'),
        ('completed', 'Завершён'),
        ('cancelled', 'Отменён'),
    ]
    status = models.CharField(
    max_length=20,
    choices=STATUS_CHOICES,
    default='new',
)
    work_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'Repair #{self.id} - {self.car}'

class Part(models.Model):
    repair = models.ForeignKey(
        Repair,
        on_delete=models.CASCADE,
        related_name='parts',
    )
    name = models.CharField(max_length=150)
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.name} x{self.quantity}'

class SparePart(models.Model):
    name = models.CharField(max_length=150)
    article = models.CharField(max_length=50, unique=True)
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name} ({self.article})'

class RepairSparePart(models.Model):
    repair = models.ForeignKey(
        Repair,
        on_delete=models.CASCADE,
        related_name='spare_parts',
    )
    spare_part = models.ForeignKey(
        SparePart,
        on_delete=models.PROTECT,
        related_name='repair_usages',
    )
    quantity = models.PositiveIntegerField(default=1)
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.spare_part.name} x{self.quantity} for repair #{self.repair_id}'

class Service(models.Model):
    name = models.CharField(max_length=150)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class RepairService(models.Model):
    repair = models.ForeignKey(
        Repair,
        on_delete=models.CASCADE,
        related_name='repair_services',
    )
    service = models.ForeignKey(
        Service,
        on_delete=models.PROTECT,
        related_name='repair_services',
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.service.name} - {self.price}'

class Balance(models.Model):
    repair = models.OneToOneField(
        Repair,
        on_delete=models.CASCADE,
        related_name='balance',
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Balance for repair #{self.repair_id}: {self.amount}'
