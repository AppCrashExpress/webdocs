from django.shortcuts import render, redirect
from django.urls      import reverse
from django.contrib   import messages

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
