from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import DeliveryMethod, Order
from .serializers import DeliveryMethodSerializer, OrderCreateSerializer


class DeliveryMethodListView(generics.ListAPIView):
    queryset = DeliveryMethod.objects.all()
    serializer_class = DeliveryMethodSerializer


class OrderCreateView(APIView):
    def post(self, request):
        serializer = OrderCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Order create successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderUpdateStatusView(APIView):
    def patch(self, request, pk, order_status):
        try:
            order = Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)

        if order_status not in ['success', 'failed']:
            return Response({'error': 'Invalid status'}, status=status.HTTP_400_BAD_REQUEST)

        order.status = order_status
        order.save()
        return Response({'message': 'Order updated successfully'}, status=status.HTTP_200_OK)
