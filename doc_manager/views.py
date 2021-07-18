from django.shortcuts import render, get_object_or_404
from django.views     import generic
from django.urls      import reverse
from . import models as the_models

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
