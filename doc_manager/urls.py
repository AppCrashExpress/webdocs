from django.urls import path
from . import views

app_name = 'doc_manager'
urlpatterns = [
    path('specification/new', views.create_specification, name='new_specification'),
    path('order/new', views.create_order, name='new_order'),
]
