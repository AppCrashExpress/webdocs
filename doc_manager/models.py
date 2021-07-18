from django.db import models
from softdelete.models import SoftDeleteObject

class Address(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class Customer(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class Material(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class VehicleModel(models.Model):
    model = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.model

class Vehicle(models.Model):
    car_id = models.CharField(max_length=255, primary_key=True)
    model  = models.ForeignKey('VehicleModel', on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ['car_id']

class Driver(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Specification(SoftDeleteObject, models.Model):
    UNITS = (
        ('m3', 'Кубические метры'),
        ('t',  'Тонны'),
    )

    class Meta:
        ordering = ['doc_no']

    doc_no    = models.PositiveIntegerField(primary_key=True)
    date      = models.DateField()
    from_addr = models.ForeignKey('Address',  on_delete=models.PROTECT, related_name='spec_from_addr')
    to_addr   = models.ForeignKey('Address',  on_delete=models.PROTECT, related_name='spec_to_addr')
    material  = models.ForeignKey('Material', on_delete=models.PROTECT)
    units     = models.CharField(max_length=3, choices=UNITS)
    price     = models.PositiveIntegerField()

class Order(SoftDeleteObject, models.Model):
    date          = models.DateField()
    specification = models.ForeignKey('Specification', on_delete=models.PROTECT)
    customer      = models.ForeignKey('Customer',      on_delete=models.PROTECT)
    count         = models.PositiveIntegerField()

    vehicle        = models.ForeignKey('Vehicle', on_delete=models.PROTECT, null=True)
    driver         = models.ForeignKey('Driver',  on_delete=models.PROTECT, null=True)
    real_from_addr = models.ForeignKey('Address', on_delete=models.PROTECT, related_name='real_from_addr', null=True)
    real_to_addr   = models.ForeignKey('Address', on_delete=models.PROTECT, related_name='real_to_addr', null=True)

    @property
    def price(self):
        return self.specification.price * self.count

    class Meta:
        ordering = ['id']
        unique_together = (('customer', 'specification'),)
