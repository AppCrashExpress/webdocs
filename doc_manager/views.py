from django.shortcuts import render, get_object_or_404
from django.views     import generic
from django.urls      import reverse
from . import models as the_models
from . import forms  as the_forms

def get_or_create_object(Model, value, request):
    try:
        obj = Model.objects.get(name=request.POST[value])
    except Model.DoesNotExist:
        obj = Model(name=request.POST[value])
        obj.save()
    return obj

class SpecificationsView(generic.ListView):
    model = the_models.Specification

    def get_queryset(self):
        from_addr = self.request.GET.get('from-addr')
        to_addr   = self.request.GET.get('to-addr')
        material  = self.request.GET.get('material')

        new_query = self.model.objects.all()
        if from_addr:
            new_query = new_query.filter(from_addr__name__icontains=from_addr)
        if to_addr:
            new_query = new_query.filter(to_addr__name__icontains=to_addr)
        if material:
            new_query = new_query.filter(material__name__icontains=material)
        return new_query


    paginate_by = 20

def create_specification(request):
    error_text = None

    if request.method == "POST":
        from_addr = get_or_create_object(the_models.Address, "from_addr", request)
        to_addr   = get_or_create_object(the_models.Address, "to_addr", request)
        material  = get_or_create_object(the_models.Material, "material", request)

        doc_no = request.POST["doc_no"]
        date   = request.POST["creation_date"]
        units  = request.POST["units"]
        price  = request.POST["price"]

        spec = the_models.Specification(
            doc_no=doc_no,
            date=date,
            from_addr=from_addr,
            to_addr=to_addr,
            material=material,
            units=units,
            price=price
        )
        
        spec.full_clean()
        spec.save()

    context = {
        'action':        reverse('doc_manager:new_specification'),
        'address_list':  the_models.Address.objects.all(), 
        'material_list': the_models.Material.objects.all(),
        'unit_options':  the_models.Specification.UNITS,
        'error_text':    error_text,
    }
    return render(request, 'doc_manager/specification.html', context=context)

def edit_specification(request, pk):
    specification = get_object_or_404(the_models.Specification, pk=pk)
    error_text = None

    if request.method == "POST":
        from_addr = get_or_create_object(the_models.Address, "from_addr", request)
        to_addr   = get_or_create_object(the_models.Address, "to_addr", request)
        material  = get_or_create_object(the_models.Material, "material", request)

        doc_no = request.POST["doc_no"]
        date  =  request.POST["creation_date"]
        units =  request.POST["units"]
        price =  request.POST["price"]

        specification.from_addr = from_addr
        specification.to_addr   = to_addr
        specification.material  = material
        specification.doc_no    = doc_no
        specification.date      = date
        specification.units     = units
        specification.price     = price

        specification.full_clean()
        specification.save()


    action = reverse('doc_manager:edit_specification',
                     kwargs={'pk': specification.pk})
    context = {
        'action':        action,
        'spec':          specification,
        'address_list':  the_models.Address.objects.all(), 
        'material_list': the_models.Material.objects.all(),
        'unit_options':  the_models.Specification.UNITS,
        'error_text':    error_text,
    }
    return render(request, 'doc_manager/specification.html', context=context)

class OrderList(generic.ListView):
    model = the_models.Order

    paginate_by = 20

def create_order(request):

    if request.method == "POST":
        customer      = get_or_create_object(the_models.Customer, "client", request)
        specification = the_models.Specification.objects.get(pk=request.POST["spec-id"])
        item_count    = request.POST["count"]
        date          = request.POST["creation_date"]

        order = the_models.Order(
            customer=customer,
            specification=specification,
            count=item_count,
            date=date
        )

        order.full_clean()
        order.save()
    
    context = {
        'action':             reverse('doc_manager:new_order'),
        'customer_list':      the_models.Customer.objects.all(),
        'specification_list': the_models.Specification.objects.all(),
    }
    return render(request, 'doc_manager/order.html', context=context)

def edit_order(request, pk):
    order = get_object_or_404(the_models.Order, pk=pk)

    if request.method == "POST":
        customer      = get_or_create_object(the_models.Customer, "client", request)
        specification = the_models.Specification.objects.get(pk=request.POST["spec-id"])
        item_count    = request.POST["count"]
        date          = request.POST["creation_date"]


        order.customer      = customer
        order.specification = specification
        order.count         = item_count
        order.date          = date

        order.full_clean()
        order.save()
    
    action = reverse('doc_manager:edit_order',
                     kwargs={'pk': order.pk})
    context = {
        'action':             action,
        'order':              order,
        'customer_list':      the_models.Customer.objects.all(),
        'specification_list': the_models.Specification.objects.all(),
    }
    return render(request, 'doc_manager/order.html', context=context)

class AddressList(generic.ListView):
    model = the_models.Address

    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_path_name'] = 'doc_manager:new_address'
        context['edit_path_name'] = 'doc_manager:edit_address'

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
    context = {
        'action': action,
        'form':   form,
    }

    return render(request, 'doc_manager/create_edit_generic.html', context=context)

class MaterialsList(generic.ListView):
    model = the_models.Material

    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_path_name'] = 'doc_manager:new_material'
        context['edit_path_name'] = 'doc_manager:edit_material'

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
    context = {
        'action': action,
        'form':   form,
    }

    return render(request, 'doc_manager/create_edit_generic.html', context=context)

class PathCostList(generic.ListView):
    model = the_models.PathCost

    paginate_by = 20

def create_path(request):

    if request.method == "POST":
        from_addr = get_or_create_object(the_models.Address, "from_addr", request)
        to_addr   = get_or_create_object(the_models.Address, "to_addr", request)

        cost = request.POST["cost"]
        
        pathcost = the_models.PathCost(
            path_from=from_addr,
            path_to=to_addr, 
            cost=cost
        )

        pathcost.full_clean()
        pathcost.save()

    context = {
        'action':        reverse('doc_manager:new_pathcost'),
        'address_list':  the_models.Address.objects.all(), 
    }

    return render(request, 'doc_manager/pathcost.html', context=context)

def edit_path(request, pk):
    pathcost = get_object_or_404(the_models.PathCost, pk=pk)

    if request.method == "POST":
        from_addr = get_or_create_object(the_models.Address, "from_addr", request)
        to_addr   = get_or_create_object(the_models.Address, "to_addr", request)

        cost = request.POST["cost"]
        
        pathcost.path_from = from_addr
        pathcost.path_to   = to_addr
        pathcost.cost      = cost

        pathcost.full_clean()
        pathcost.save()

    action = reverse('doc_manager:edit_pathcost', kwargs={"pk": pathcost.pk})

    context = {
        'action':        action,
        'address_list':  the_models.Address.objects.all(), 
        'pathcost':      pathcost,
    }

    return render(request, 'doc_manager/pathcost.html', context=context)
