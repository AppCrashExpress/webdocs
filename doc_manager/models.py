from django.db         import models
from django.db.models  import Sum, F, Q
from safedelete.models import SafeDeleteModel

class Address(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

class Contractor(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

class PathCost(models.Model):
    path_from  = models.ForeignKey(Address, on_delete=models.PROTECT, related_name='path_from')
    path_to    = models.ForeignKey(Address, on_delete=models.PROTECT, related_name='path_to')
    cost       = models.PositiveIntegerField()
    contractor = models.ForeignKey(Contractor, on_delete=models.PROTECT, null=True, blank=True)

    class Meta:
        ordering = ['path_from', 'path_to']
        constraints = [
            models.UniqueConstraint(
                fields=['path_from', 'path_to', 'contractor'],
                name='pathcost_unique_definition'
            ),
            models.CheckConstraint(
                check=~Q(path_from=F('path_to')),
                name='pathcost_path_not_loop'
            ),
        ]

    def clean(self):
        # Using PostgreSQL, NULL is not equal NULL, so constraint 
        # with null will always pass. Manually check in this case
        from django.core.exceptions import ValidationError
        if self.contractor is None: 
            obj_exists = PathCost.objects.filter(
                    path_from=self.path_from,
                    path_to=self.path_to,
                    contractor__isnull=True
                ).exists()

            if obj_exists:
                raise ValidationError('Путь с такими адресами уже существует')

    def __str__(self):
        string = f'Из "{self.path_from}" в "{self.path_to}" со стоимостью {self.cost}'
        if self.contractor:
            string += f' и подрядчиком {self.contractor}'
        return string

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
    car_id = models.CharField(max_length=255, unique=True)
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

class Specification(SafeDeleteModel, models.Model):
    UNITS = (
        ('m3', 'Кубические метры'),
        ('t',  'Тонны'),
    )

    doc_no    = models.PositiveIntegerField(unique=True)
    date      = models.DateField()
    customer  = models.ForeignKey(Customer, on_delete=models.PROTECT)
    from_addr = models.ForeignKey(Address,  on_delete=models.PROTECT, related_name='spec_from_addr')
    to_addr   = models.ForeignKey(Address,  on_delete=models.PROTECT, related_name='spec_to_addr')
    material  = models.ForeignKey(Material, on_delete=models.PROTECT)
    units     = models.CharField(max_length=3, choices=UNITS)
    price     = models.PositiveIntegerField()

    class Meta:
        ordering = ['doc_no']
        permissions = [
            ("undelete_specification",    'Есть возможность восстанавливать спецификации, помеченные на удаление'),
            ("hard_delete_specification", 'Есть возможность удалять спецификации, помеченные на удаление')
        ]
        constraints = [
            models.UniqueConstraint(
                fields=['customer', 'from_addr', 'to_addr', 'material', 'units'],
                name='specification_unique_definition'
            ),
            models.CheckConstraint(
                check=~Q(from_addr=F('to_addr')),
                name='specification_path_not_loop'
            ),
        ]

    def __str__(self):
        return (f'Спец. №{self.doc_no} {self.date} заказчика {self.customer}, '
                f'из {self.from_addr} в {self.to_addr}, '
                f'{self.material} {self.get_units_display()}')

class Execution(models.Model):
    exec_no  = models.PositiveIntegerField(unique=True)
    date     = models.DateField()

    class Meta:
        ordering = ['exec_no']

    def __str__(self):
        return (f'Исполн. №{self.exec_no} {self.date} '
                f'с {self.order_set.count()} заказами')

class ContractorExecution(models.Model):
    exec_no    = models.PositiveIntegerField()
    date       = models.DateField()
    contractor = models.ForeignKey(Contractor, on_delete=models.PROTECT)

    class Meta:
        ordering = ['exec_no', 'contractor']
        constraints = [
            models.UniqueConstraint(
                fields=['exec_no', 'contractor'],
                name='cont_exec_unique_definition'
            ),
        ]

    def __str__(self):
        return (f'Исполн. №{self.exec_no} {self.date} подрядчика '
                f'{self.contractor} '
                f'с {self.order_set.count()} заказами')

class Order(SafeDeleteModel, models.Model):
    date          = models.DateField()
    specification = models.ForeignKey(Specification, on_delete=models.PROTECT)
    count         = models.PositiveIntegerField()

    driver     = models.ForeignKey(Driver,     on_delete=models.PROTECT, null=True, blank=True)
    contractor = models.ForeignKey(Contractor, on_delete=models.PROTECT, null=True, blank=True)

    vehicle = models.ForeignKey(Vehicle,  on_delete=models.PROTECT, null=True, blank=True)
    path    = models.ForeignKey(PathCost, on_delete=models.PROTECT, null=True, blank=True)

    exec_doc = models.ForeignKey(Execution, on_delete=models.SET_NULL, null=True, blank=True)
    contr_doc = models.ForeignKey(ContractorExecution, on_delete=models.SET_NULL, null=True, blank=True)

    @property
    def price(self):
        return self.specification.price * self.count

    class Meta:
        ordering = ['id']
        permissions = [
            ("undelete_order",    'Есть возможность восстанавливать заказы, помеченные на удаление'),
            ("hard_delete_order", 'Есть возможность удалять заказы, помеченные на удаление')
        ]
        constraints = [
            models.CheckConstraint(
                check=(Q(driver__isnull=True) | Q(contractor__isnull=True)),
                name="order_not_both_drivers"
            ),
            models.CheckConstraint(
                check=(Q(exec_doc__isnull=True) | Q(contr_doc__isnull=True)),
                name="order_not_both_docs"
            ),
        ]

    def __str__(self):
        return f'Заказ с № спец. {self.specification.doc_no} по пути: {self.path}'
