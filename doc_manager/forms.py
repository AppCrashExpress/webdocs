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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False

class MaterialForm(ModelForm):
    class Meta:
        model = the_models.Material
        fields = ['name']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False

class CustomerForm(ModelForm):
    class Meta:
        model = the_models.Customer
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False

class VehicleForm(ModelForm):
    class Meta:
        model = the_models.Vehicle
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False

class DriverForm(ModelForm):
    class Meta:
        model = the_models.Driver
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False

class ContractorForm(ModelForm):
    class Meta:
        model = the_models.Contractor
        fields = ['name']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False

class PathCostForm(ModelForm):
    class Meta:
        model = the_models.PathCost
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False

    def clean(self):
        cleaned_data = super().clean()

        path_from = cleaned_data.get('path_from')
        path_to   = cleaned_data.get('path_to')

        if path_from == path_to:
            raise ValidationError('Начальный и конечный пути не должны совпадать')

        return cleaned_data

class SpecificationForm(ModelForm):
    class Meta:
        model = the_models.Specification
        fields = '__all__'
        widgets = {
            'date': DateInput(format=('%Y-%m-%d'),
                              attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False

    def clean(self):
        cleaned_data = super().clean()

        from_addr = cleaned_data.get('from_addr')
        to_addr   = cleaned_data.get('to_addr')

        if from_addr == to_addr:
            raise ValidationError('Начальный и конечный пути не должны совпадать')

        return cleaned_data

class OrderForm(ModelForm):
    class Meta:
        model = the_models.Order
        fields = [
            'date',
            'specification',
            'count',
            'driver',
            'contractor',
            'vehicle',
            'path',
        ]
        widgets = {
            'date': DateInput(format=('%Y-%m-%d'),
                              attrs={'type': 'date'}),
            'specification': RadioSelect(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False

    def clean(self):
        cleaned_data = super().clean()

        driver = cleaned_data.get('driver')
        contractor = cleaned_data.get('contractor')
        path = cleaned_data.get('path')
        vehicle = cleaned_data.get('vehicle')

        if path is None and driver is None and contractor is None:
            return cleaned_data
        elif path is None:
            raise ValidationError("Если выбран либо водитель, либо подрядчик, "
                                  "то путь должен быть выбран")

        if driver is not None and contractor is not None:
            raise ValidationError("Можно выбрать либо водителя, либо подрядчика")
        elif driver is None and contractor is None:
            raise ValidationError("Нужно выбрать водителя или подрядчика")

        if driver is not None and vehicle is None:
            raise ValidationError("К водителю нужно выбрать транспорт")

        if contractor != path.contractor:
            raise ValidationError('Подрядчик должен совпадать с указанным в пути')

        return cleaned_data

class ExecutionMultipleChoiceField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        label = (f'<th scope="row">{obj.pk}</td>'
                f'<td>{obj.date}</td>'
                f'<td>{obj.specification.from_addr}</td>'
                f'<td>{obj.specification.to_addr}</td>'
                f'<td>{obj.specification.doc_no}</td>'
                f'<td>{obj.price}</td>')
        label += f'<td>{obj.contractor}</td>' if obj.contractor else '<td></td>'
        label += f'<td>{obj.specification.customer}</td>'
        return label

class ExecutionForm(ModelForm):
    class Meta:
        model  = the_models.Execution
        fields = '__all__'
        widgets = {
            'date': DateInput(format=('%Y-%m-%d'),
                              attrs={'type': 'date'}),
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

        self.fields['orders'].queryset = the_models.Order.objects.filter(
                order_filter
            )

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

        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)

        if commit == True:
            instance.save()
            instance.order_set.update(exec_doc=None)
            self.cleaned_data['orders'].update(exec_doc=instance.pk)

        return instance

class ContractorExecutionForm(ModelForm):
    class Meta:
        model  = the_models.ContractorExecution
        fields = '__all__'
        widgets = {
            'date': DateInput(format=('%Y-%m-%d'),
                              attrs={'type': 'date'}),
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

        order_filter = Q(contr_doc__isnull=True)
        if self.instance.pk:
            order_filter |= Q(contr_doc=self.instance.pk)

        self.fields['orders'].queryset = the_models.Order.objects.filter(
                order_filter & Q(contractor__isnull=False)
            )

        if self.instance.pk:
            self.fields['orders'].initial = self.instance.order_set.all()

    def clean(self):
        cleaned_data = super().clean()

        data = cleaned_data.get('orders')
        selected_contractor = cleaned_data.get('contractor')

        if not data or len(data) == 0:
            raise ValidationError("Должен быть выбран хотя бы один заказ")

        distinct_contractors = data.order_by('contractor__id') \
                                .values('contractor') \
                                .distinct()
        if len(distinct_contractors) != 1:
            raise ValidationError("У выбранных заказов должен быть один подрядчик")

        contractor_id = distinct_contractors[0]['contractor'] 

        if contractor_id != selected_contractor.id:
            raise ValidationError("Подрядчик у закакзов должен совпадать с выбранным")

        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)

        if commit == True:
            instance.save()
            instance.order_set.update(contr_doc=None)
            self.cleaned_data['orders'].update(contr_doc=instance.pk)

        return instance

