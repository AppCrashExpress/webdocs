from django.db import models

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

class Specification(models.Model):
    UNITS = (
        ('cm3', 'Cubic centimeters'),
        ('t',   'Tonnes'),
    )

    number    = models.PositiveIntegerField()
    from_addr = models.ForeignKey('Address',  on_delete=models.PROTECT, related_name='spec_from_addr')
    to_addr   = models.ForeignKey('Address',  on_delete=models.PROTECT, related_name='spec_to_addr')
    material  = models.ForeignKey('Material', on_delete=models.PROTECT)
    units     = models.CharField(max_length=3, choices=UNITS)
    price     = models.PositiveIntegerField()

class Order(models.Model):
    customer      = models.ForeignKey('Customer',      on_delete=models.PROTECT)
    specification = models.ForeignKey('Specification', on_delete=models.PROTECT)
    count         = models.PositiveIntegerField()

    class Meta:
        unique_together = (('customer', 'specification'),)

class VehicleModel(models.Model):
    model = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.model

class Vehicle(models.Model):
    car_id = models.CharField(max_length=255, primary_key=True)
    model  = models.ForeignKey('VehicleModel', on_delete=models.SET_NULL, null=True)

class Driver(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Execution(models.Model):
    order     = models.ForeignKey('Order',    on_delete=models.PROTECT)
    vehicle   = models.ForeignKey('Vehicle',  on_delete=models.PROTECT, null=True)
    driver    = models.ForeignKey('Driver',   on_delete=models.PROTECT, null=True)
    from_addr = models.ForeignKey('Address',  on_delete=models.PROTECT, related_name='ord_from_addr', null=True)
    to_addr   = models.ForeignKey('Address',  on_delete=models.PROTECT, related_name='ord_to_addr', null=True)
