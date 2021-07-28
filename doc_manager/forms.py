from django.forms        import ModelForm, DateInput, RadioSelect
from crispy_forms.helper import FormHelper
from . import models as the_models

class AddressForm(ModelForm):
    class Meta:
        model = the_models.Address
        fields = ['name']
        labels = {
            'name': 'Полный адрес',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False

class MaterialForm(ModelForm):
    class Meta:
        model = the_models.Material
        fields = ['name']
        labels = {
            'name': 'Материал',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False

class CustomerForm(ModelForm):
    class Meta:
        model = the_models.Customer
        fields = '__all__'
        labels = {
            'name': 'Клиент',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False

class VehicleForm(ModelForm):
    class Meta:
        model = the_models.Vehicle
        fields = '__all__'
        labels = {
            'car_id': 'Номер',
            'model':  'Модель',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False

class DriverForm(ModelForm):
    class Meta:
        model = the_models.Driver
        fields = '__all__'
        labels = {
            'name': 'ФИО',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False

class PathCostForm(ModelForm):
    class Meta:
        model = the_models.PathCost
        fields = '__all__'
        labels = {
            'path_from': 'Начало пути',
            'path_from': 'Конец пути',
            'cost':      'Ставка',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False

class SpecificationForm(ModelForm):
    class Meta:
        model = the_models.Specification
        fields = '__all__'
        widgets = {
            'date': DateInput(format=('%Y-%m-%d'),
                              attrs={'type': 'date'}),
        }
        labels = {
            'doc_no':    'Номер документа',
            'date':      'Дата создания',
            'from_addr': 'Начальный адрес',
            'to_addr':   'Конечный адрес',
            'material':  'Материал',
            'units':     'Единицы измерения',
            'price':     'Цена',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False

class OrderForm(ModelForm):
    class Meta:
        model = the_models.Order
        fields = '__all__'
        widgets = {
            'date': DateInput(format=('%Y-%m-%d'),
                              attrs={'type': 'date'}),
            'specification': RadioSelect(),
        }
        labels = {
            'date':          'Дата создания',
            'specification': 'Спецификация',
            'customer':      'Клиент',
            'count':         'Количество',
            'vehicle':       'Машина',
            'driver':        'Водитель',
            'path':          'Путь',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
