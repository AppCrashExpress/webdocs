from django.urls import path
from . import views

app_name = 'doc_manager'
urlpatterns = [
    path('specifications/', views.SpecificationsView.as_view(), name='specification'),
    path('specifications/new/', views.create_specification, name='new_specification'),
    path('specifications/<int:pk>/', views.edit_specification, name='edit_specification'),
    path('orders/', views.OrderList.as_view(), name='order'),
    path('orders/new/', views.create_order, name='new_order'),
    path('orders/<int:pk>/', views.edit_order, name='edit_order'),
    path('addresses/', views.AddressList.as_view(), name='address'),
    path('addresses/new/', views.create_address, name='new_address'),
    path('addresses/<int:pk>/', views.edit_address, name='edit_address'),
    path('materials/', views.MaterialsList.as_view(), name='material'),
    path('materials/new/', views.create_material, name='new_material'),
    path('materials/<int:pk>/', views.edit_material, name='edit_material'),
    path('customers/', views.CustomersList.as_view(), name='customer'),
    path('customers/new/', views.create_customer, name='new_customer'),
    path('customers/<int:pk>/', views.edit_customer, name='edit_customer'),
    path('vehicles/', views.VehiclesList.as_view(), name='vehicle'),
    path('vehicles/new/', views.create_vehicle, name='new_vehicle'),
    path('vehicles/<int:pk>/', views.edit_vehicle, name='edit_vehicle'),
    path('drivers/', views.DriversList.as_view(), name='driver'),
    path('drivers/new/', views.create_driver, name='new_driver'),
    path('drivers/<int:pk>/', views.edit_driver, name='edit_driver'),
    path('paths/', views.PathCostList.as_view(), name='pathcost'),
    path('paths/new', views.create_path, name='new_pathcost'),
    path('paths/<int:pk>', views.edit_path, name='edit_pathcost'),
]
