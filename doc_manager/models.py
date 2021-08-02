from django.db         import models
from django.db.models  import Sum, F, Q
from safedelete.models import SafeDeleteModel

class Address(models.Model):
    name = models.CharField("Полный адрес", max_length=255, unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

class Contractor(models.Model):
    name = models.CharField("Подрядчик", max_length=255)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

class PathCost(models.Model):
    path_from = models.ForeignKey(
                            Address,
                            on_delete=models.PROTECT,
                            related_name='path_from',
                            verbose_name="Начало пути")
    path_to = models.ForeignKey(
                            Address,
                            on_delete=models.PROTECT,
                            related_name='path_to',
                            verbose_name="Конец пути")
    contractor = models.ForeignKey(
                            Contractor,
                            on_delete=models.PROTECT,
                            null=True,
                            blank=True,
                            verbose_name="Подрядчик")
    cost = models.PositiveIntegerField("Ставка")

    class Meta:
        verbose_name = "Путь со ставкой"
        verbose_name_plural = "Пути со ставками"
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
    name = models.CharField("Клиент", max_length=255, unique=True)

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"
        ordering = ['name']

    def __str__(self):
        return self.name

class Material(models.Model):
    name = models.CharField("Материал", max_length=255, unique=True)

    class Meta:
        verbose_name = "Материал"
        verbose_name_plural = "Материалы"
        ordering = ['name']

    def __str__(self):
        return self.name

class Vehicle(models.Model):
    car_id = models.CharField("Гос. номер", max_length=255, unique=True)
    model  = models.CharField("Модель", max_length=255)

    class Meta:
        verbose_name = "Транспорт"
        verbose_name_plural = "Транспорты"
        ordering = ['car_id']

    def __str__(self):
        return f'"{self.car_id}": {self.model}'

class Driver(models.Model):
    name = models.CharField("ФИО", max_length=255)

    class Meta:
        verbose_name = "Водитель"
        verbose_name_plural = "Водители"
        ordering = ['name']

    def __str__(self):
        return self.name

class Specification(SafeDeleteModel, models.Model):
    UNITS = (
        ('m3', 'м3'),
        ('t',  'т'),
    )

    doc_no    = models.PositiveIntegerField("Номер", unique=True)
    date      = models.DateField("Дата создания")
    units     = models.CharField("Ед. изм.", max_length=3, choices=UNITS)
    price     = models.PositiveIntegerField("Цена за ед.")
    customer  = models.ForeignKey(
                            Customer,
                            on_delete=models.PROTECT,
                            verbose_name="Клиент")
    from_addr = models.ForeignKey(
                            Address,
                            on_delete=models.PROTECT,
                            related_name='spec_from_addr',
                            verbose_name="Начало пути")
    to_addr   = models.ForeignKey(
                            Address,
                            on_delete=models.PROTECT,
                            related_name='spec_to_addr',
                            verbose_name="Конец пути")
    material  = models.ForeignKey(
                            Material,
                            on_delete=models.PROTECT,
                            verbose_name="Материал")

    class Meta:
        verbose_name = "Спецификация"
        verbose_name_plural = "Спецификации"
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
    exec_no  = models.PositiveIntegerField("Номер", unique=True)
    date     = models.DateField("Дата создания")

    class Meta:
        verbose_name = "УПД"
        verbose_name_plural = "УПД"
        ordering = ['exec_no']

    def __str__(self):
        return (f'Исполн. №{self.exec_no} {self.date} '
                f'с {self.order_set.count()} заказами')

class ContractorExecution(models.Model):
    exec_no    = models.PositiveIntegerField("Номер")
    date       = models.DateField("Дата создания")
    contractor = models.ForeignKey(
                            Contractor,
                            on_delete=models.PROTECT,
                            verbose_name="Подрядчик")

    class Meta:
        verbose_name = "УПД подрядчика"
        verbose_name_plural = "УПД подрядчика"
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
    date          = models.DateField("Дата создания")
    count         = models.PositiveIntegerField("Количество")
    specification = models.ForeignKey(
                            Specification,
                            on_delete=models.PROTECT,
                            verbose_name="Номер спец.")

    driver     = models.ForeignKey(
                            Driver,
                            on_delete=models.PROTECT,
                            null=True,
                            blank=True,
                            verbose_name="Водитель")
    contractor = models.ForeignKey(
                            Contractor,
                            on_delete=models.PROTECT,
                            null=True,
                            blank=True,
                            verbose_name="Подрядчик")

    vehicle = models.ForeignKey(
                            Vehicle,
                            on_delete=models.PROTECT,
                            null=True,
                            blank=True,
                            verbose_name="Транспорт")
    path    = models.ForeignKey(
                            PathCost,
                            on_delete=models.PROTECT,
                            null=True,
                            blank=True,
                            verbose_name="Путь")

    exec_doc  = models.ForeignKey(
                            Execution,
                            on_delete=models.SET_NULL,
                            null=True,
                            blank=True,
                            verbose_name="Номер УПД")
    contr_doc = models.ForeignKey(
                            ContractorExecution,
                            on_delete=models.SET_NULL,
                            null=True,
                            blank=True,
                            verbose_name="Номер УПД подрядчика")

    @property
    def price(self):
        return self.specification.price * self.count

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
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
