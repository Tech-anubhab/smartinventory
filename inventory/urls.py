from django.urls import path
from . import views

urlpatterns = [
    path("", views.item_list, name="inventory_list"),
    path("add/", views.item_create, name="inventory_create"),
    path("<int:pk>/edit/", views.item_update, name="inventory_update"),
    path("<int:pk>/delete/", views.item_delete, name="inventory_delete"),
    path("<int:pk>/sell/", views.item_sell, name="inventory_sell"),
    path("reset/", views.reset_inventory, name="inventory_reset"),
    path('sales/', views.sales_report, name='sales_report'),
]

