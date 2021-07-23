from django.shortcuts import render, redirect, get_object_or_404
from django.views     import generic
from django.urls      import reverse
from . import models as the_models
from . import forms  as the_forms

class SpecificationsView(generic.ListView):
    model = the_models.Specification
    paginate_by = 20

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
    if request.method == "POST":
        form = the_forms.SpecificationForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = the_forms.SpecificationForm()

    context = {
        'action': reverse('doc_manager:new_specification'),
        'form':   form,
    }

    return render(request, 'doc_manager/create_edit_generic.html', context=context)

def edit_specification(request, pk):
    spec = the_models.Specification.objects.get(pk=pk)

    if request.method == "POST":
        form = the_forms.SpecificationForm(request.POST, instance=spec)
        if form.is_valid():
            form.save()
    else:
        form = the_forms.SpecificationForm(instance=spec)

    action = reverse('doc_manager:edit_specification',
                     kwargs={'pk':spec.pk})

    
    delete_action = reverse('doc_manager:delete_specification',
                     kwargs={'pk':spec.pk})
    
    related_objs = spec.order_set.all()

    context = {
        'delete_action':        delete_action,
        'related_objects_list': related_objs,
        'action': action,
        'form':   form,
    }

    return render(request, 'doc_manager/create_edit_generic.html', context=context)

def delete_specification(request, pk):
    spec = the_models.Specification.objects.get(pk=pk)
    spec.delete()
    return redirect('doc_manager:specification')

class OrderList(generic.ListView):
    model = the_models.Order
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_path_name'] = 'doc_manager:new_order'
        context['edit_path_name'] = 'doc_manager:edit_order'

        return context

def create_order(request):
    if request.method == "POST":
        form = the_forms.OrderForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = the_forms.OrderForm()

    context = {
        'action':             reverse('doc_manager:new_order'),
        'form':               form,
        'specification_list': the_models.Specification.objects.all(),
    }

    return render(request, 'doc_manager/order.html', context=context)

def edit_order(request, pk):
    order = the_models.Order.objects.get(pk=pk)

    if request.method == "POST":
        form = the_forms.OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
    else:
        form = the_forms.OrderForm(instance=order)

    action = reverse('doc_manager:edit_order',
                     kwargs={'pk':order.pk})

    delete_action = reverse('doc_manager:delete_order',
                     kwargs={'pk':order.pk})

    context = {
        'action':             action,
        'delete_action':      delete_action,
        'form':               form,
        'specification_list': the_models.Specification.objects.all(),
    }
    return render(request, 'doc_manager/order.html', context=context)

def delete_order(request, pk):
    order = the_models.Order.objects.get(pk=pk)
    order.delete()
    return redirect('doc_manager:order')

class AddressList(generic.ListView):
    model = the_models.Address
    paginate_by = 20

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
    if request.method == "POST":
        form = the_forms.AddressForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = the_forms.AddressForm()

    context = {
        'action': reverse('doc_manager:new_address'),
        'form':   form,
    }

    return render(request, 'doc_manager/create_edit_generic.html', context=context)

def edit_address(request, pk):
    address = the_models.Address.objects.get(pk=pk)

    if request.method == "POST":
        form = the_forms.AddressForm(request.POST, instance=address)
        if form.is_valid():
            form.save()
    else:
        form = the_forms.AddressForm(instance=address)

    action = reverse('doc_manager:edit_address',
                     kwargs={'pk':address.pk})

    delete_action = reverse('doc_manager:delete_address',
                     kwargs={'pk':address.pk})

    context = {
        'delete_action': delete_action,
        'action': action,
        'form':   form,
    }

    return render(request, 'doc_manager/create_edit_generic.html', context=context)

def delete_address(request, pk):
    address = the_models.Address.objects.get(pk=pk)
    address.delete()
    return redirect('doc_manager:address')

class MaterialsList(generic.ListView):
    model = the_models.Material
    paginate_by = 20

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
    if request.method == "POST":
        form = the_forms.MaterialForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = the_forms.MaterialForm()

    context = {
        'action': reverse('doc_manager:new_material'),
        'form':   form,
    }

    return render(request, 'doc_manager/create_edit_generic.html', context=context)

def edit_material(request, pk):
    material = the_models.Material.objects.get(pk=pk)

    if request.method == "POST":
        form = the_forms.MaterialForm(request.POST, instance=material)
        if form.is_valid():
            form.save()
    else:
        form = the_forms.MaterialForm(instance=material)

    action = reverse('doc_manager:edit_material',
                     kwargs={'pk':material.pk})

    delete_action = reverse('doc_manager:delete_material',
                     kwargs={'pk':material.pk})

    context = {
        'delete_action': delete_action,
        'action': action,
        'form':   form,
    }

    return render(request, 'doc_manager/create_edit_generic.html', context=context)

def delete_material(request, pk):
    material = the_models.Material.objects.get(pk=pk)
    material.delete()
    return redirect('doc_manager:material')

class CustomersList(generic.ListView):
    model = the_models.Customer
    paginate_by = 20

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
    if request.method == "POST":
        form = the_forms.CustomerForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = the_forms.CustomerForm()

    context = {
        'action': reverse('doc_manager:new_customer'),
        'form':   form,
    }

    return render(request, 'doc_manager/create_edit_generic.html', context=context)

def edit_customer(request, pk):
    customer = the_models.Customer.objects.get(pk=pk)

    if request.method == "POST":
        form = the_forms.CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
    else:
        form = the_forms.CustomerForm(instance=customer)

    action = reverse('doc_manager:edit_customer',
                     kwargs={'pk':customer.pk})

    delete_action = reverse('doc_manager:delete_customer',
                     kwargs={'pk':customer.pk})

    context = {
        'delete_action': delete_action,
        'action': action,
        'form':   form,
    }

    return render(request, 'doc_manager/create_edit_generic.html', context=context)

def delete_customer(request, pk):
    customer = the_models.Customer.objects.get(pk=pk)
    customer.delete()
    return redirect('doc_manager:customer')

class VehiclesList(generic.ListView):
    model = the_models.Vehicle
    paginate_by = 20

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
    if request.method == "POST":
        form = the_forms.VehicleForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = the_forms.VehicleForm()

    context = {
        'action': reverse('doc_manager:new_vehicle'),
        'form':   form,
    }

    return render(request, 'doc_manager/create_edit_generic.html', context=context)

def edit_vehicle(request, pk):
    vehicle = the_models.Vehicle.objects.get(pk=pk)

    if request.method == "POST":
        form = the_forms.VehicleForm(request.POST, instance=vehicle)
        if form.is_valid():
            form.save()
    else:
        form = the_forms.VehicleForm(instance=vehicle)

    action = reverse('doc_manager:edit_vehicle',
                     kwargs={'pk':vehicle.pk})

    delete_action = reverse('doc_manager:delete_vehicle',
                     kwargs={'pk':vehicle.pk})

    context = {
        'delete_action': delete_action,
        'action': action,
        'form':   form,
    }

    return render(request, 'doc_manager/create_edit_generic.html', context=context)

def delete_vehicle(request, pk):
    vehicle = the_models.Vehicle.objects.get(pk=pk)
    vehicle.delete()
    return redirect('doc_manager:vehicle')

class DriversList(generic.ListView):
    model = the_models.Driver
    paginate_by = 20

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
    if request.method == "POST":
        form = the_forms.DriverForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = the_forms.DriverForm()

    context = {
        'action': reverse('doc_manager:new_driver'),
        'form':   form,
    }

    return render(request, 'doc_manager/create_edit_generic.html', context=context)

def edit_driver(request, pk):
    driver = the_models.Driver.objects.get(pk=pk)

    if request.method == "POST":
        form = the_forms.DriverForm(request.POST, instance=driver)
        if form.is_valid():
            form.save()
    else:
        form = the_forms.DriverForm(instance=driver)

    action = reverse('doc_manager:edit_driver',
                     kwargs={'pk':driver.pk})

    delete_action = reverse('doc_manager:delete_driver',
                     kwargs={'pk':driver.pk})

    context = {
        'delete_action': delete_action,
        'action': action,
        'form':   form,
    }

    return render(request, 'doc_manager/create_edit_generic.html', context=context)

def delete_driver(request, pk):
    driver = the_models.Driver.objects.get(pk=pk)
    driver.delete()
    return redirect('doc_manager:driver')

class PathCostList(generic.ListView):
    model = the_models.PathCost
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_path_name'] = 'doc_manager:new_pathcost'
        context['edit_path_name'] = 'doc_manager:edit_pathcost'

        return context

def create_path(request):
    if request.method == "POST":
        form = the_forms.PathCostForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = the_forms.PathCostForm()

    context = {
        'action': reverse('doc_manager:new_pathcost'),
        'form':   form,
    }

    return render(request, 'doc_manager/create_edit_generic.html', context=context)

def edit_path(request, pk):
    pathcost = the_models.PathCost.objects.get(pk=pk)
    if request.method == "POST":
        form = the_forms.PathCostForm(request.POST, instance=pathcost)
        if form.is_valid():
            form.save()
    else:
        form = the_forms.PathCostForm(instance=pathcost)

    action = reverse('doc_manager:edit_pathcost',
                     kwargs={'pk':pathcost.pk})

    delete_action = reverse('doc_manager:delete_pathcost',
                     kwargs={'pk':pathcost.pk})

    context = {
        'delete_action': delete_action,
        'action': action,
        'form':   form,
    }

    return render(request, 'doc_manager/create_edit_generic.html', context=context)

def delete_path(request, pk):
    path = the_models.PathCost.objects.get(pk=pk)
    path.delete()
    return redirect('doc_manager:pathcost')

