from rest_framework import generics
from .models import DeliveryMethod
from .serializers import DeliveryMethodSerializer


class DeliveryMethodListView(generics.ListAPIView):
    queryset = DeliveryMethod.objects.all()
    serializer_class = DeliveryMethodSerializer
