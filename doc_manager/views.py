from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins     import PermissionRequiredMixin

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib   import messages
from django.views     import generic
from django.urls      import reverse

from django.db.models import Sum, F, Q

from safedelete.models import HARD_DELETE

from . import models as the_models
from . import forms  as the_forms
from .utils import create_generic, edit_generic, delete_generic

class SpecificationsView(generic.ListView):
    model = the_models.Specification

    def get_queryset(self):
        from_addr = self.request.GET.get('from-addr', '')
        to_addr   = self.request.GET.get('to-addr', '')
        material  = self.request.GET.get('material', '')

        queryset = self.model.objects.all()
        queryset = queryset.filter(from_addr__name__icontains=from_addr)
        queryset = queryset.filter(to_addr__name__icontains=to_addr)
        queryset = queryset.filter(material__name__icontains=material)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_path_name'] = 'doc_manager:new_specification'
        context['edit_path_name'] = 'doc_manager:edit_specification'

        context['from_addr'] = self.request.GET.get('from-addr', '')
        context['to_addr']   = self.request.GET.get('to-addr', '')
        context['material']  = self.request.GET.get('material', '')

        return context

def create_specification(request):
    return create_generic(
        request,
        form_class=the_forms.SpecificationForm,
        create_path_name='doc_manager:new_specification',
        edit_path_name='doc_manager:edit_specification',
        template_name='doc_manager/create_edit_generic.html'
    )

def edit_specification(request, pk):
    spec = the_models.Specification.objects.get(pk=pk)
    related_objs = spec.order_set.all()

    return edit_generic(
        request, pk,
        form_class=the_forms.SpecificationForm,
        model_class=the_models.Specification,
        edit_path_name='doc_manager:edit_specification',
        delete_path_name='doc_manager:delete_specification',
        template_name='doc_manager/create_edit_generic.html',
        context_args={
            'related_objects_list': related_objs,
        }
    )

def delete_specification(request, pk):
    return delete_generic(
        request, pk,
        model_class=the_models.Specification,
        list_url_name='doc_manager:specification'
    )

class DeletedSpecificationsView(PermissionRequiredMixin, generic.ListView):
    model = the_models.Specification
    permission_required = [
        'doc_manager.undelete_specification',
        'doc_manager.hard_delete_specification',
    ]

    def get_queryset(self):
        from_addr = self.request.GET.get('from-addr', '')
        to_addr   = self.request.GET.get('to-addr', '')
        material  = self.request.GET.get('material', '')

        queryset = self.model.objects.deleted_only()
        queryset = queryset.filter(from_addr__name__icontains=from_addr)
        queryset = queryset.filter(to_addr__name__icontains=to_addr)
        queryset = queryset.filter(material__name__icontains=material)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['edit_path_name'] = 'doc_manager:restore_specification'

        context['from_addr'] = self.request.GET.get('from-addr', '')
        context['to_addr']   = self.request.GET.get('to-addr', '')
        context['material']  = self.request.GET.get('material', '')

        return context

@permission_required('doc_manager.undelete_specification')
def restore_specification(request, pk):
    spec = the_models.Specification.objects.deleted_only().get(pk=pk)

    if request.method == "POST":
        form = the_forms.SpecificationForm(request.POST, instance=spec)
        if form.is_valid():
            form.save()

            message = f'Восстановлено: {form.instance}'
            messages.success(request, message)

            return redirect('doc_manager:edit_specification', pk=form.instance.pk)
    else:
        form = the_forms.SpecificationForm(instance=spec)

    action = reverse('doc_manager:restore_specification',
                     kwargs={'pk':spec.pk})
    
    delete_action = reverse('doc_manager:hard_delete_specification',
                     kwargs={'pk':spec.pk})
    
    context = {
        'delete_action': delete_action,
        'action':        action,
        'form':          form,
    }

    return render(request, 'doc_manager/create_edit_generic.html', context=context)

@permission_required('doc_manager.hard_delete_specification')
def hard_delete_specification(request, pk):
    spec = the_models.Specification.objects.deleted_only().get(pk=pk)
    spec_str = str(spec)
    spec.delete(force_policy=HARD_DELETE)

    message = f'Удалено: {spec_str}'
    messages.success(request, message)

    return redirect('doc_manager:deleted_specification')

class OrderList(generic.ListView):
    model = the_models.Order

    def get_queryset(self):
        start_date_value = self.request.GET.get('start_date')
        end_date_value   = self.request.GET.get('end_date')
        get_unfinished_orders = self.request.GET.get('unfinished_orders')

        queryset = self.model.objects.all()
        if start_date_value:
            queryset = queryset.filter(date__gte=start_date_value)
        if end_date_value:
            queryset = queryset.filter(date__lte=end_date_value)
        if get_unfinished_orders:
            queryset = queryset.filter(
                Q(driver__isnull=True) & Q(contractor__isnull=True) 
                | Q(path__isnull=True)
            )

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_path_name'] = 'doc_manager:new_order'
        context['edit_path_name'] = 'doc_manager:edit_order'

        context['start_date_value']  = self.request.GET.get('start_date', '')
        context['end_date_value']    = self.request.GET.get('end_date', '')
        context['unfinished_orders'] = self.request.GET.get('unfinished_orders', '')

        return context

def create_order(request):
    return create_generic(
        request,
        form_class=the_forms.OrderForm,
        create_path_name='doc_manager:new_order',
        edit_path_name='doc_manager:edit_order',
        template_name='doc_manager/order.html',
        context_args={
            'specification_list': the_models.Specification.objects.all(),
        }
    )

def edit_order(request, pk):
    return edit_generic(
        request, pk,
        form_class=the_forms.OrderForm,
        model_class=the_models.Order,
        edit_path_name='doc_manager:edit_order',
        delete_path_name='doc_manager:delete_order',
        template_name='doc_manager/order.html',
        context_args={
            'specification_list': the_models.Specification.objects.all(),
        }
    )

def delete_order(request, pk):
    order = the_models.Order.objects.get(pk=pk)

    if order.exec_doc is not None:
        message = f'Невозможно удалить, так как заказ связан с УПД'
        messages.error(request, message)
        return redirect('doc_manager:edit_order', pk=order.pk)

    if order.contr_doc is not None:
        message = f'Невозможно удалить, так как заказ связан с УПД подрядчика'
        messages.error(request, message)
        return redirect('doc_manager:edit_order', pk=order.pk)

    order_str = str(order)
    order.delete()
    message = f'Удалено: {order_str}'
    messages.success(request, message)

    return redirect('doc_manager:order')

class OrderReportList(generic.ListView):
    model = the_models.Order
    template_name="doc_manager/order_report.html"

    def get_queryset(self):
        customer_id      = self.request.GET.get('customer')
        start_date_value = self.request.GET.get('start_date')
        end_date_value   = self.request.GET.get('end_date')

        queryset = self.model.objects.all()
        if customer_id:
            queryset = queryset.filter(specification__customer=customer_id)
        if start_date_value:
            queryset = queryset.filter(date__gte=start_date_value)
        if end_date_value:
            queryset = queryset.filter(date__lte=end_date_value)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['customer_list']    = the_models.Customer.objects.all()
        context['customer_value']   = self.request.GET.get('customer', '')
        context['start_date_value'] = self.request.GET.get('start_date', '')
        context['end_date_value']   = self.request.GET.get('end_date', '')

        totals = self.get_queryset().aggregate(
            metres_total=Sum('count', filter=Q(specification__units='m3')),
            tonnes_total=Sum('count', filter=Q(specification__units='t')),
            metres_sum=Sum(F('specification__price') * F('count'), filter=Q(specification__units='m3')),
            tonnes_sum=Sum(F('specification__price') * F('count'), filter=Q(specification__units='t')),
        )
        for key, value in totals.items():
            context[key] = 0 if value is None else value

        context['total_sum'] = context['metres_sum'] + context['tonnes_sum']

        return context

class DeletedOrderList(PermissionRequiredMixin, generic.ListView):
    model = the_models.Order
    permission_required = [
        'doc_manager.undelete_order',
        'doc_manager.hard_delete_order',
    ]

    def get_queryset(self):
        queryset = self.model.objects.deleted_only()
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['edit_path_name'] = 'doc_manager:restore_order'

        return context

@permission_required('doc_manager.undelete_order')
def restore_order(request, pk):
    order = the_models.Order.objects.deleted_only().get(pk=pk)

    if request.method == "POST":
        form = the_forms.OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()

            message = f'Восстановлено: {form.instance}'
            messages.success(request, message)

            return redirect('doc_manager:edit_order', pk=form.instance.pk)
    else:
        form = the_forms.OrderForm(instance=order)

    action = reverse('doc_manager:restore_order',
                     kwargs={'pk':order.pk})

    delete_action = reverse('doc_manager:hard_delete_order',
                     kwargs={'pk':order.pk})

    context = {
        'action':             action,
        'delete_action':      delete_action,
        'form':               form,
        'specification_list': the_models.Specification.objects.all(),
    }
    return render(request, 'doc_manager/order.html', context=context)

@permission_required('doc_manager.hard_delete_order')
def hard_delete_order(request, pk):
    order = the_models.Order.objects.deleted_only().get(pk=pk)
    order_str = str(order)
    order.delete(force_policy=HARD_DELETE)

    message = f'Удалено: {order_str}'
    messages.success(request, message)

    return redirect('doc_manager:deleted_order')

class ExecutionList(generic.ListView):
    model = the_models.Execution

    def get_queryset(self):
        customer_id      = self.request.GET.get('customer')
        start_date_value = self.request.GET.get('start_date')
        end_date_value   = self.request.GET.get('end_date')

        queryset = self.model.objects.all()

        if customer_id:
            queryset = queryset.filter(order__specification__customer=customer_id)
        if start_date_value:
            queryset = queryset.filter(date__gte=start_date_value)
        if end_date_value:
            queryset = queryset.filter(date__lte=end_date_value)

        queryset = queryset.annotate(
            customer=F('order__specification__customer__name'),
            sum=Sum(F('order__count') * F('order__specification__price'))
        )

        queryset = queryset.order_by('date', 'customer')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_path_name'] = 'doc_manager:new_execution'
        context['edit_path_name'] = 'doc_manager:edit_execution'

        context['customer_list']    = the_models.Customer.objects.all()
        context['customer_value']   = self.request.GET.get('customer', '')
        context['start_date_value'] = self.request.GET.get('start_date', '')
        context['end_date_value']   = self.request.GET.get('end_date', '')

        return context

def create_execution(request):
    return create_generic(
        request,
        form_class=the_forms.ExecutionForm,
        create_path_name='doc_manager:new_execution',
        edit_path_name='doc_manager:edit_execution',
        template_name='doc_manager/execution.html'
    )

def edit_execution(request, pk):
    return edit_generic(
        request, pk,
        form_class=the_forms.ExecutionForm,
        model_class=the_models.Execution,
        edit_path_name='doc_manager:edit_execution',
        delete_path_name='doc_manager:delete_execution',
        template_name='doc_manager/execution.html',
    )

def delete_execution(request, pk):
    return delete_generic(
        request, pk,
        model_class=the_models.Execution,
        list_url_name='doc_manager:execution'
    )

class ContractorExecutionList(generic.ListView):
    model = the_models.ContractorExecution
    template_name = 'doc_manager/contractor_execution_list.html'

    def get_queryset(self):
        contractor_id    = self.request.GET.get('contractor')
        start_date_value = self.request.GET.get('start_date')
        end_date_value   = self.request.GET.get('end_date')

        queryset = self.model.objects.all()

        if contractor_id:
            queryset = queryset.filter(contractor=contractor_id)
        if start_date_value:
            queryset = queryset.filter(date__gte=start_date_value)
        if end_date_value:
            queryset = queryset.filter(date__lte=end_date_value)

        queryset = queryset.annotate(
            sum=Sum(F('order__count') * F('order__specification__price'))
        )

        queryset = queryset.order_by('date', 'order__contractor')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_path_name'] = 'doc_manager:new_contractor_execution'
        context['edit_path_name'] = 'doc_manager:edit_contractor_execution'

        context['contractor_list']  = the_models.Contractor.objects.all()
        context['contractor_value'] = self.request.GET.get('contractor', '')
        context['start_date_value'] = self.request.GET.get('start_date', '')
        context['end_date_value']   = self.request.GET.get('end_date', '')

        return context

def create_contractor_execution(request):
    return create_generic(
        request,
        form_class=the_forms.ContractorExecutionForm,
        create_path_name='doc_manager:new_contractor_execution',
        edit_path_name='doc_manager:edit_contractor_execution',
        template_name='doc_manager/contractor_execution.html'
    )

def edit_contractor_execution(request, pk):
    return edit_generic(
        request, pk,
        form_class=the_forms.ContractorExecutionForm,
        model_class=the_models.ContractorExecution,
        edit_path_name='doc_manager:edit_contractor_execution',
        delete_path_name='doc_manager:delete_contractor_execution',
        template_name='doc_manager/contractor_execution.html',
    )

def delete_contractor_execution(request, pk):
    return delete_generic(
        request, pk,
        model_class=the_models.ContractorExecution,
        list_url_name='doc_manager:contractor_execution'
    )

class AddressList(generic.ListView):
    model = the_models.Address

    def get_queryset(self):
        name_value = self.request.GET.get('name', '')
        queryset = self.model.objects.filter(name__icontains=name_value)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_path_name'] = 'doc_manager:new_address'
        context['edit_path_name'] = 'doc_manager:edit_address'

        context['name_value'] = self.request.GET.get('name', '')

        return context

def create_address(request):
    return create_generic(
        request,
        form_class=the_forms.AddressForm,
        create_path_name='doc_manager:new_address',
        edit_path_name='doc_manager:edit_address',
        template_name='doc_manager/create_edit_generic.html'
    )

def edit_address(request, pk):
    return edit_generic(
        request, pk,
        form_class=the_forms.AddressForm,
        model_class=the_models.Address,
        edit_path_name='doc_manager:edit_address',
        delete_path_name='doc_manager:delete_address',
        template_name='doc_manager/create_edit_generic.html',
    )

def delete_address(request, pk):
    return delete_generic(
        request, pk,
        model_class=the_models.Address,
        list_url_name='doc_manager:address'
    )

class MaterialsList(generic.ListView):
    model = the_models.Material

    def get_queryset(self):
        name_value = self.request.GET.get('name', '')
        queryset = self.model.objects.filter(name__icontains=name_value)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_path_name'] = 'doc_manager:new_material'
        context['edit_path_name'] = 'doc_manager:edit_material'

        context['name_value'] = self.request.GET.get('name', '')

        return context

def create_material(request):
    return create_generic(
        request,
        form_class=the_forms.MaterialForm,
        create_path_name='doc_manager:new_material',
        edit_path_name='doc_manager:edit_material',
        template_name='doc_manager/create_edit_generic.html'
    )

def edit_material(request, pk):
    return edit_generic(
        request, pk,
        form_class=the_forms.MaterialForm,
        model_class=the_models.Material,
        edit_path_name='doc_manager:edit_material',
        delete_path_name='doc_manager:delete_material',
        template_name='doc_manager/create_edit_generic.html',
    )

def delete_material(request, pk):
    return delete_generic(
        request, pk,
        model_class=the_models.Material,
        list_url_name='doc_manager:material'
    )

class CustomersList(generic.ListView):
    model = the_models.Customer

    def get_queryset(self):
        name_value = self.request.GET.get('name', '')
        queryset = self.model.objects.filter(name__icontains=name_value)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_path_name'] = 'doc_manager:new_customer'
        context['edit_path_name'] = 'doc_manager:edit_customer'

        context['name_value'] = self.request.GET.get('name', '')

        return context

def create_customer(request):
    return create_generic(
        request,
        form_class=the_forms.CustomerForm,
        create_path_name='doc_manager:new_customer',
        edit_path_name='doc_manager:edit_customer',
        template_name='doc_manager/create_edit_generic.html'
    )

def edit_customer(request, pk):
    return edit_generic(
        request, pk,
        form_class=the_forms.CustomerForm,
        model_class=the_models.Customer,
        edit_path_name='doc_manager:edit_customer',
        delete_path_name='doc_manager:delete_customer',
        template_name='doc_manager/create_edit_generic.html',
    )

def delete_customer(request, pk):
    return delete_generic(
        request, pk,
        model_class=the_models.Customer,
        list_url_name='doc_manager:customer'
    )

class VehiclesList(generic.ListView):
    model = the_models.Vehicle

    def get_queryset(self):
        car_id_value = self.request.GET.get('car-id', '')
        model_value  = self.request.GET.get('model', '')

        queryset = self.model.objects.all()
        queryset = queryset.filter(car_id__icontains=car_id_value)
        queryset = queryset.filter(model__icontains=model_value)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_path_name'] = 'doc_manager:new_vehicle'
        context['edit_path_name'] = 'doc_manager:edit_vehicle'

        context['car_id_value'] = self.request.GET.get('car-id', '')
        context['model_value']  = self.request.GET.get('model', '')

        return context

def create_vehicle(request):
    return create_generic(
        request,
        form_class=the_forms.VehicleForm,
        create_path_name='doc_manager:new_vehicle',
        edit_path_name='doc_manager:edit_vehicle',
        template_name='doc_manager/create_edit_generic.html'
    )

def edit_vehicle(request, pk):
    return edit_generic(
        request, pk,
        form_class=the_forms.VehicleForm,
        model_class=the_models.Vehicle,
        edit_path_name='doc_manager:edit_vehicle',
        delete_path_name='doc_manager:delete_vehicle',
        template_name='doc_manager/create_edit_generic.html',
    )

def delete_vehicle(request, pk):
    return delete_generic(
        request, pk,
        model_class=the_models.Vehicle,
        list_url_name='doc_manager:vehicle'
    )

class DriversList(generic.ListView):
    model = the_models.Driver

    def get_queryset(self):
        name_value = self.request.GET.get('name', '')
        queryset = self.model.objects.filter(name__icontains=name_value)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_path_name'] = 'doc_manager:new_driver'
        context['edit_path_name'] = 'doc_manager:edit_driver'

        context['name_value'] = self.request.GET.get('name', '')

        return context

def create_driver(request):
    return create_generic(
        request,
        form_class=the_forms.DriverForm,
        create_path_name='doc_manager:new_driver',
        edit_path_name='doc_manager:edit_driver',
        template_name='doc_manager/create_edit_generic.html'
    )

def edit_driver(request, pk):
    return edit_generic(
        request, pk,
        form_class=the_forms.DriverForm,
        model_class=the_models.Driver,
        edit_path_name='doc_manager:edit_driver',
        delete_path_name='doc_manager:delete_driver',
        template_name='doc_manager/create_edit_generic.html',
    )

def delete_driver(request, pk):
    return delete_generic(
        request, pk,
        model_class=the_models.Driver,
        list_url_name='doc_manager:driver'
    )

class DriverReportList(generic.ListView):
    model = the_models.Order
    template_name="doc_manager/driver_report.html"

    def get_queryset(self):
        driver_id        = self.request.GET.get('driver')
        start_date_value = self.request.GET.get('start_date')
        end_date_value   = self.request.GET.get('end_date')

        queryset = self.model.objects.filter(path__isnull=False)
        queryset = queryset.filter(driver__isnull=False)

        if driver_id:
            queryset = queryset.filter(driver=driver_id)
        if start_date_value:
            queryset = queryset.filter(date__gte=start_date_value)
        if end_date_value:
            queryset = queryset.filter(date__lte=end_date_value)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['driver_list']      = the_models.Driver.objects.all()
        context['driver_value']     = self.request.GET.get('driver', '')
        context['start_date_value'] = self.request.GET.get('start_date', '')
        context['end_date_value']   = self.request.GET.get('end_date', '')

        context['total'] = self.get_queryset().aggregate(
            total=Sum('path__cost')
        )['total']

        return context

class ContractorsList(generic.ListView):
    model = the_models.Contractor

    def get_queryset(self):
        name_value = self.request.GET.get('name', '')
        queryset = self.model.objects.filter(name__icontains=name_value)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_path_name'] = 'doc_manager:new_contractor'
        context['edit_path_name'] = 'doc_manager:edit_contractor'

        context['name_value'] = self.request.GET.get('name', '')

        return context

def create_contractor(request):
    return create_generic(
        request,
        form_class=the_forms.ContractorForm,
        create_path_name='doc_manager:new_contractor',
        edit_path_name='doc_manager:edit_contractor',
        template_name='doc_manager/create_edit_generic.html'
    )

def edit_contractor(request, pk):
    return edit_generic(
        request, pk,
        form_class=the_forms.ContractorForm,
        model_class=the_models.Contractor,
        edit_path_name='doc_manager:edit_contractor',
        delete_path_name='doc_manager:delete_contractor',
        template_name='doc_manager/create_edit_generic.html',
    )

def delete_contractor(request, pk):
    return delete_generic(
        request, pk,
        model_class=the_models.Contractor,
        list_url_name='doc_manager:contractor'
    )

class ContractorReportList(generic.ListView):
    model = the_models.Order
    template_name="doc_manager/contractor_report.html"

    def get_queryset(self):
        contractor_id    = self.request.GET.get('contractor')
        start_date_value = self.request.GET.get('start_date')
        end_date_value   = self.request.GET.get('end_date')

        queryset = self.model.objects.filter(path__isnull=False)
        queryset = queryset.filter(contractor__isnull=False)

        if contractor_id:
            queryset = queryset.filter(contractor=contractor_id)
        if start_date_value:
            queryset = queryset.filter(date__gte=start_date_value)
        if end_date_value:
            queryset = queryset.filter(date__lte=end_date_value)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['contractor_list']  = the_models.Contractor.objects.all()
        context['contractor_value'] = self.request.GET.get('contractor', '')
        context['start_date_value'] = self.request.GET.get('start_date', '')
        context['end_date_value']   = self.request.GET.get('end_date', '')

        context['total'] = self.get_queryset().aggregate(
            total=Sum('path__cost')
        )['total']

        return context

class PathCostList(generic.ListView):
    model = the_models.PathCost

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_path_name'] = 'doc_manager:new_pathcost'
        context['edit_path_name'] = 'doc_manager:edit_pathcost'

        return context

def create_path(request):
    return create_generic(
        request,
        form_class=the_forms.PathCostForm,
        create_path_name='doc_manager:new_pathcost',
        edit_path_name='doc_manager:edit_pathcost',
        template_name='doc_manager/create_edit_generic.html'
    )

def edit_path(request, pk):
    return edit_generic(
        request, pk,
        form_class=the_forms.PathCostForm,
        model_class=the_models.PathCost,
        edit_path_name='doc_manager:edit_pathcost',
        delete_path_name='doc_manager:delete_pathcost',
        template_name='doc_manager/create_edit_generic.html',
    )

def delete_path(request, pk):
    return delete_generic(
        request, pk,
        model_class=the_models.PathCost,
        list_url_name='doc_manager:pathcost'
    )
