from django.urls import path
from django.views.generic.base import TemplateView
from . import views

app_name = 'doc_manager'
urlpatterns = [
    path('', TemplateView.as_view(template_name="base_generic.html")),

    path('specifications/', views.SpecificationsView.as_view(), name='specification'),
    path('specifications/new/', views.create_specification, name='new_specification'),
    path('specifications/<int:pk>/', views.edit_specification, name='edit_specification'),
    path('specifications/<int:pk>/delete/', views.delete_specification,
          name='delete_specification'),

    path('specifications/deleted/', views.DeletedSpecificationsView.as_view(), name='deleted_specification'),
    path('specifications/deleted/<int:pk>/', views.restore_specification, name='restore_specification'),
    path('specifications/deleted/<int:pk>/delete/', views.hard_delete_specification,
          name='hard_delete_specification'),

    path('orders/', views.OrderList.as_view(), name='order'),
    path('orders/new/', views.create_order, name='new_order'),
    path('orders/<int:pk>/', views.edit_order, name='edit_order'),
    path('orders/<int:pk>/delete/', views.delete_order, name='delete_order'),
    path('orders/report/', views.OrderReportList.as_view(), name='order_report'),
    path('orders/report/download/', views.download_order_report, name='order_report_download'),

    path('execution/', views.ExecutionList.as_view(), name='execution'),
    path('execution/new/', views.create_execution, name='new_execution'),
    path('execution/<int:pk>/', views.edit_execution, name='edit_execution'),
    path('execution/<int:pk>/delete/', views.delete_execution, name='delete_execution'),

    path('orders/deleted/', views.DeletedOrderList.as_view(), name='deleted_order'),
    path('orders/deleted/<int:pk>/', views.restore_order, name='restore_order'),
    path('orders/deleted/<int:pk>/delete/', views.hard_delete_order, name='hard_delete_order'),

    path('addresses/', views.AddressList.as_view(), name='address'),
    path('addresses/new/', views.create_address, name='new_address'),
    path('addresses/<int:pk>/', views.edit_address, name='edit_address'),
    path('addresses/<int:pk>/delete/', views.delete_address, name='delete_address'),

    path('materials/', views.MaterialsList.as_view(), name='material'),
    path('materials/new/', views.create_material, name='new_material'),
    path('materials/<int:pk>/', views.edit_material, name='edit_material'),
    path('materials/<int:pk>/delete/', views.delete_material, name='delete_material'),

    path('customers/', views.CustomersList.as_view(), name='customer'),
    path('customers/new/', views.create_customer, name='new_customer'),
    path('customers/<int:pk>/', views.edit_customer, name='edit_customer'),
    path('customers/<int:pk>/delete/', views.delete_customer, name='delete_customer'),

    path('vehicles/', views.VehiclesList.as_view(), name='vehicle'),
    path('vehicles/new/', views.create_vehicle, name='new_vehicle'),
    path('vehicles/<int:pk>/', views.edit_vehicle, name='edit_vehicle'),
    path('vehicles/<int:pk>/delete/', views.delete_vehicle, name='delete_vehicle'),

    path('drivers/', views.DriversList.as_view(), name='driver'),
    path('drivers/new/', views.create_driver, name='new_driver'),
    path('drivers/<int:pk>/', views.edit_driver, name='edit_driver'),
    path('drivers/<int:pk>/delete/', views.delete_driver, name='delete_driver'),
    path('drivers/report/', views.DriverReportList.as_view(), name='driver_report'),
    path('drivers/report/download/', views.download_driver_report, name='driver_report_download'),

    path('contractor/', views.ContractorsList.as_view(), name='contractor'),
    path('contractor/new/', views.create_contractor, name='new_contractor'),
    path('contractor/<int:pk>/', views.edit_contractor, name='edit_contractor'),
    path('contractor/<int:pk>/delete/', views.delete_contractor, name='delete_contractor'),
    path('contractor/report/', views.ContractorReportList.as_view(), name='contractor_report'),
    path('contractor/report/download/', views.download_contractor_report, name='contractor_report_download'),

    path('contractor/execution/', 
         views.ContractorExecutionList.as_view(),
         name='contractor_execution'),
    path('contractor/execution/new/',
         views.create_contractor_execution,
         name='new_contractor_execution'),
    path('contractor/execution/<int:pk>/',
         views.edit_contractor_execution,
         name='edit_contractor_execution'),
    path('contractor/execution/<int:pk>/delete/',
         views.delete_contractor_execution,
         name='delete_contractor_execution'),

    path('paths/', views.PathCostList.as_view(), name='pathcost'),
    path('paths/new/', views.create_path, name='new_pathcost'),
    path('paths/<int:pk>/', views.edit_path, name='edit_pathcost'),
    path('paths/<int:pk>/delete/', views.delete_path, name='delete_pathcost'),
]
