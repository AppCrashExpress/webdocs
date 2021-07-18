from django.db         import models
from softdelete.models import SoftDeleteObject

class Address(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

class PathCost(models.Model):
    path_from = models.ForeignKey('Address', on_delete=models.PROTECT, related_name='path_from')
    path_to   = models.ForeignKey('Address', on_delete=models.PROTECT, related_name='path_to')
    cost      = models.PositiveIntegerField()

    class Meta:
        ordering = ['path_from', 'path_to']
        unique_together = (('path_from', 'path_to'),)

    def __str__(self):
        return f'"{self.path_from.name}" to "{self.path_to.name} with cost {self.cost}'

class Customer(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

class Material(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

class Vehicle(models.Model):
    car_id = models.CharField(max_length=255, primary_key=True)
    model  = models.CharField(max_length=255)

    class Meta:
        ordering = ['car_id']

    def __str__(self):
        return f'"{self.car_id}": {self.model}'

class Driver(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

class Specification(SoftDeleteObject, models.Model):
    UNITS = (
        ('m3', 'Кубические метры'),
        ('t',  'Тонны'),
    )

    doc_no    = models.PositiveIntegerField(primary_key=True)
    date      = models.DateField()
    from_addr = models.ForeignKey('Address',  on_delete=models.PROTECT, related_name='spec_from_addr')
    to_addr   = models.ForeignKey('Address',  on_delete=models.PROTECT, related_name='spec_to_addr')
    material  = models.ForeignKey('Material', on_delete=models.PROTECT)
    units     = models.CharField(max_length=3, choices=UNITS)
    price     = models.PositiveIntegerField()

    class Meta:
        ordering = ['doc_no']
        unique_together = (('from_addr', 'to_addr'),)

class Order(SoftDeleteObject, models.Model):
    date          = models.DateField()
    specification = models.ForeignKey('Specification', on_delete=models.PROTECT)
    customer      = models.ForeignKey('Customer',      on_delete=models.PROTECT)
    count         = models.PositiveIntegerField()

    vehicle = models.ForeignKey('Vehicle',  on_delete=models.PROTECT, null=True, blank=True)
    driver  = models.ForeignKey('Driver',   on_delete=models.PROTECT, null=True, blank=True)
    path    = models.ForeignKey('PathCost', on_delete=models.PROTECT, null=True, blank=True)

    @property
    def price(self):
        return self.specification.price * self.count

    class Meta:
        ordering = ['id']
        unique_together = (('customer', 'specification'),)
