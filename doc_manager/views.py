from django.shortcuts import render
from . import models as the_models

def create_specification(request):
    def get_or_create_object(Model, value):
        try:
            obj = Model.objects.get(name=request.POST[value])
        except Model.DoesNotExist:
            obj = Model(name=request.POST[value])
            obj.save()
        return obj

    error_text = None

    if request.method == "POST":
        from_addr = get_or_create_object(the_models.Address,  "from_addr")
        to_addr   = get_or_create_object(the_models.Address,  "to_addr")
        material  = get_or_create_object(the_models.Material, "material")

        doc_no = request.POST["doc_no"]
        units =  request.POST["units"]
        price =  request.POST["price"]

        spec = the_models.Specification(
            number=doc_no,
            from_addr=from_addr,
            to_addr=to_addr,
            material=material,
            units=units,
            price=price
        )
        
        spec.full_clean()
        spec.save()

    context = {
        'address_list':  the_models.Address.objects.all(), 
        'material_list': the_models.Material.objects.all(),
        'unit_options':  the_models.Specification.UNITS,
        'error_text':    error_text,
    }
    return render(request, 'doc_manager/new_specification.html', context=context)
