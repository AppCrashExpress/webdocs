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
    path('paths/', views.PathCostList.as_view(), name='pathcost'),
    path('paths/new', views.create_path, name='new_pathcost'),
    path('paths/<int:pk>', views.edit_path, name='edit_pathcost'),
]
