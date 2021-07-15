from django.urls import path
from . import views

app_name = 'doc_manager'
urlpatterns = [
    path('specifications/', views.SpecificationsView.as_view(), name='specification'),
    path('specifications/new/', views.create_specification, name='new_specification'),
    path('specifications/<int:pk>/', views.edit_specification, name='edit_specification'),
    path('orders/new/', views.create_order, name='new_order'),
]
