import datetime
from itertools import chain

from django.shortcuts import render, redirect
from django.urls      import reverse
from django.contrib   import messages
from openpyxl import Workbook

def create_generic(
    request, *, form_class,
    create_path_name, edit_path_name, template_name,
    context_args={}
):
    if request.method == "POST":
        form = form_class(request.POST)
        if form.is_valid():
            form.save()

            message = f'Создано: {form.instance}'
            messages.success(request, message)

            return redirect(edit_path_name, pk=form.instance.pk)

    else:
        form = form_class()

    context = {
        'action': reverse(create_path_name),
        'form':   form,
        **context_args,
    }

    return render(request, template_name, context=context)

def edit_generic(
    request, pk, *, form_class, model_class,
    edit_path_name, delete_path_name, template_name,
    context_args={}
):
    instance = model_class.objects.get(pk=pk)

    if request.method == "POST":
        form = form_class(request.POST, instance=instance)
        if form.is_valid():
            form.save()

            message = f'Изменено: {form.instance}'
            messages.success(request, message)
    else:
        form = form_class(instance=instance)

    action = reverse(edit_path_name,
                     kwargs={'pk':instance.pk})

    
    delete_action = reverse(delete_path_name,
                     kwargs={'pk':instance.pk})
    
    context = {
        'delete_action': delete_action,
        'action':        action,
        'form':          form,
        **context_args,
    }

    return render(request, template_name, context=context)

def delete_generic(request, pk, *, model_class, list_url_name):
    instance = model_class.objects.get(pk=pk)
    inst_str = str(instance)
    instance.delete()

    message = f'Удалено: {inst_str}'
    messages.success(request, message)

    return redirect(list_url_name)

def get_verbose_name(model, string):
    # Stackoverflow 52410442
    fields = string.split('__')

    for field_name in fields[:-1]:
        field = model._meta.get_field(field_name)

        if field.many_to_one:
            model = field.foreign_related_fields[0].model
        elif field.many_to_many or field.one_to_one or field.one_to_many:
            model = field.related_model
        else:
            raise ValueError(f'Field not found: {field_name}')

    return model._meta.get_field(fields[-1]).verbose_name

def get_report_workbook(queryset, *, fields, verbose_names, display_values):
    def normalize_value(value, display_values):
        # Can modify if new special types arise
        if value is None:
            return ""

        if isinstance(value, datetime.date):
            return value.strftime('%d.%m.%Y')

        dv = display_values.get(value, None)
        if dv:
            return dv

        return str(value)

    def get_field_names(fields, vebose_names, model):
        field_names = []

        for field in fields:
            vb_name = verbose_names.get(field, None)
            if vb_name is None:
                vb_name = get_verbose_name(model, field)

            field_names.append(vb_name)

        return field_names

    model = queryset.model
    wb = Workbook()
    ws = wb.active

    field_names = get_field_names(fields, verbose_names, model)

    ws.append(field_names)

    normalizer_func = lambda x : normalize_value(x, display_values)
    for value_set in queryset.values_list(*fields):
        normalized_set = map(normalizer_func, value_set)
        ws.append(tuple(normalized_set))

    return wb
