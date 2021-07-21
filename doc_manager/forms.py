from django.forms import ModelForm, DateInput, RadioSelect
from . import models as the_models

class AddressForm(ModelForm):
    class Meta:
        model = the_models.Address
        fields = ['name']
        labels = {
            'name': 'Полный адрес',
        }

class MaterialForm(ModelForm):
    class Meta:
        model = the_models.Material
        fields = ['name']
        labels = {
            'name': 'Материал',
        }

class CustomerForm(ModelForm):
    class Meta:
        model = the_models.Customer
        fields = '__all__'
        labels = {
            'name': 'Клиент',
        }

class VehicleForm(ModelForm):
    class Meta:
        model = the_models.Vehicle
        fields = '__all__'
        labels = {
            'car_id': 'Номер',
            'model':  'Модель',
        }

class DriverForm(ModelForm):
    class Meta:
        model = the_models.Driver
        fields = '__all__'
        labels = {
            'name': 'ФИО',
        }

class PathCostForm(ModelForm):
    class Meta:
        model = the_models.PathCost
        fields = '__all__'
        labels = {
            'path_from': 'Начало пути',
            'path_from': 'Конец пути',
            'cost':      'Ставка',
        }

class SpecificationForm(ModelForm):
    class Meta:
        model = the_models.Specification
        fields = '__all__'
        widgets = {
            'date': DateInput(attrs={'type': 'date'}),
        }
        labels = {
            'doc_no':    'Номер документа',
            'date':      'Дата создания',
            'from_addr': 'Начало пути',
            'to_addr':   'Конец пути',
            'material':  'Материал',
            'units':     'Единицы измерения',
            'price':     'Цена',
        }

class OrderForm(ModelForm):
    class Meta:
        model = the_models.Order
        fields = '__all__'
        widgets = {
            'date':          DateInput(attrs={'type': 'date'}),
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
