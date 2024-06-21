from django.urls import path
from .views import DeliveryMethodListView

urlpatterns = [
    path('delivery-methods/', DeliveryMethodListView.as_view(), name='delivery-method-list'),
]
