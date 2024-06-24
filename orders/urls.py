from django.urls import path
from .views import DeliveryMethodListView, OrderCreateView, OrderUpdateStatusView

urlpatterns = [
    path('delivery-methods/', DeliveryMethodListView.as_view(), name='delivery-method-list'),
    path('', OrderCreateView.as_view(), name='order-create'),
    path('<int:pk>/<str:order_status>/', OrderUpdateStatusView.as_view(), name='order-update-status'),

]
