from rest_framework import serializers

from products.models import Product, ProductVariation, RecommendProduct
from .models import DeliveryMethod, Order, OrderItem


class DeliveryMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryMethod
        fields = ['id', 'name', 'img', 'description', 'price']


class OrderItemSerializer(serializers.Serializer):
    variation = serializers.IntegerField()
    quantity = serializers.IntegerField()


class RecommendProductSerializer(serializers.Serializer):
    product = serializers.IntegerField()
    quantity = serializers.IntegerField()


class OrderCreateSerializer(serializers.Serializer):
    product = serializers.IntegerField()
    first_name = serializers.CharField(max_length=255)
    last_name = serializers.CharField(max_length=255)
    phone_num = serializers.CharField(max_length=20)
    email = serializers.EmailField()
    address = serializers.CharField()
    house_number = serializers.CharField(max_length=20)
    postal_code = serializers.CharField(max_length=10)
    city = serializers.CharField(max_length=255)
    delivery_method = serializers.IntegerField()
    recommend_products = serializers.ListField(child=RecommendProductSerializer(), required=False)
    order_items = serializers.ListField(child=OrderItemSerializer())

    def create(self, validated_data):
        order_items_data = validated_data.pop('order_items')
        recommend_products_data = validated_data.pop('recommend_products', [])
        product_id = validated_data.pop('product')
        delivery_method_id = validated_data.pop('delivery_method')

        product = Product.objects.get(id=product_id)
        delivery_method = DeliveryMethod.objects.get(id=delivery_method_id)

        total_amount = delivery_method.price

        for order_item_data in order_items_data:
            variation = ProductVariation.objects.get(id=order_item_data['variation'])
            total_amount += variation.product.price * order_item_data['quantity']

        for recommend_product_data in recommend_products_data:
            recommend_product = RecommendProduct.objects.get(id=recommend_product_data['product'])
            total_amount += recommend_product.price * recommend_product_data['quantity']

        order = Order.objects.create(
            product=product,
            delivery_method=delivery_method,
            status='new',
            total_amount=total_amount,
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            phone_num=validated_data['phone_num'],
            email=validated_data['email'],
            address=validated_data['address'],
            house_number=validated_data['house_number'],
            postal_code=validated_data['postal_code'],
            city=validated_data['city']
        )

        for order_item_data in order_items_data:
            variation = ProductVariation.objects.get(id=order_item_data['variation'])

            for recommend_product_data in recommend_products_data:
                recommend_product = RecommendProduct.objects.get(id=recommend_product_data['product'])
                OrderItem.objects.create(
                    order=order, recommend_product=recommend_product, quantity=recommend_product_data['quantity']
                )

            OrderItem.objects.create(order=order, variation=variation, quantity=order_item_data['quantity'])

        return order
