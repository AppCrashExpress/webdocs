from django.forms import ModelForm
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
