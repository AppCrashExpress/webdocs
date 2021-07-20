from django.forms import ModelForm
from . import models as the_models

class AddressForm(ModelForm):
    class Meta:
        model = the_models.Address
        fields = ['name']
        labels = {
            'name': 'Полный адрес',
        }
