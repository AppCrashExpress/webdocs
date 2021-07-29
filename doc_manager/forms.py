from django              import forms
from django.db.models    import Q
from django.forms        import ModelForm, DateInput, RadioSelect, CheckboxSelectMultiple
from django.core.exceptions import ValidationError
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
        fields = [
            'date',
            'specification',
            'count',
            'vehicle',
            'driver',
            'path',
        ]
        widgets = {
            'date': DateInput(format=('%Y-%m-%d'),
                              attrs={'type': 'date'}),
            'specification': RadioSelect(),
        }
        labels = {
            'date':          'Дата создания',
            'specification': 'Спецификация',
            'count':         'Количество',
            'vehicle':       'Машина',
            'driver':        'Водитель',
            'path':          'Путь',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False

class ExecutionForm(ModelForm):
    class ExecutionMultipleChoiceField(forms.ModelMultipleChoiceField):
        def label_from_instance(self, obj):
            return (f'<th scope="row">{obj.pk}</td>'
                    f'<td>{obj.date}</td>'
                    f'<td>{obj.specification.pk}</td>'
                    f'<td>{obj.specification.customer}</td>')

    class Meta:
        model  = the_models.Execution
        fields = '__all__'
        widgets = {
            'date': DateInput(format=('%Y-%m-%d'),
                              attrs={'type': 'date'}),
        }
        labels = {
            'exec_no': 'Номер УПД',
            'date':    'Дата создания',
        }

    orders = ExecutionMultipleChoiceField(
        label='Заказы',
        widget=CheckboxSelectMultiple(),
        queryset=None
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_tag = False

        order_filter = Q(exec_doc__isnull=True)
        if self.instance.pk:
            order_filter |= Q(exec_doc=self.instance.pk)
        self.fields['orders'].queryset = the_models.Order.objects.filter(order_filter)
        if self.instance.pk:
            self.fields['orders'].initial = self.instance.order_set.all()

    def clean(self):
        cleaned_data = super().clean()

        data = cleaned_data.get('orders')

        if not data or len(data) == 0:
            raise ValidationError("Должен быть выбран хотя бы один заказ")

        distinct_customers = data.order_by('specification__customer__id') \
                                .values('specification__customer') \
                                .distinct()

        if len(distinct_customers) != 1:
            raise ValidationError("У выбранных заказов должен быть один клиент")

    def save(self, commit=True):
        instance = super().save(commit=False)

        if commit == True:
            instance.save()
            instance.order_set.update(exec_doc=None)
            self.cleaned_data['orders'].update(exec_doc=instance.pk)

        return instance

