import requests

from django.conf import settings

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


class OrderItemDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id', 'variation', 'quantity', 'price']


class OrderDetailSerializer(serializers.ModelSerializer):
    order_items = OrderItemDetailsSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'product', 'first_name', 'last_name', 'phone_num', 'email', 'address', 'house_number', 'postal_code', 'city', 'delivery_method', 'status', 'total_amount', 'order_items']


import requests
from django.conf import settings
from rest_framework import serializers

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
    payment_url = serializers.URLField(read_only=True)
    payment_type = serializers.CharField(max_length=20)

    def create(self, validated_data):
        order_items_data = validated_data.pop('order_items')
        recommend_products_data = validated_data.pop('recommend_products', [])
        product_id = validated_data.pop('product')
        delivery_method_id = validated_data.pop('delivery_method')

        product = Product.objects.get(id=product_id)
        delivery_method = DeliveryMethod.objects.get(id=delivery_method_id)

        total_amount = delivery_method.price
        
        order_items_lenght = len(order_items_data)
        total_amount = 0  # Початкове значення для загальної суми

        discount = 0
        if order_items_lenght == 2:
            discount = 0.20
        elif order_items_lenght >= 3:
            discount = 0.30

        products_payload = []

        for order_item_data in order_items_data:
            variation = ProductVariation.objects.get(id=order_item_data['variation'])

            discount_price = variation.product.price * (variation.product.discount / 100)
            product_price = variation.product.price - discount_price

            price = product_price * order_item_data['quantity']

            if discount > 0:
                price -= price * discount
            total_amount += price

            products_payload.append({
                "name": variation.product.title,
                "unitPrice": int(product_price * 100),  # Сума у грошових одиницях (субодиниці валюти)
                "quantity": order_item_data['quantity']
            })

        for recommend_product_data in recommend_products_data:
            recommend_product = RecommendProduct.objects.get(id=recommend_product_data['product'])
            total_amount += recommend_product.price * recommend_product_data['quantity']

            products_payload.append({
                "name": recommend_product.name,
                "unitPrice": int(recommend_product.price * 100),  # Сума у грошових одиницях (субодиниці валюти)
                "quantity": recommend_product_data['quantity']
            })

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
            payment_type=validated_data['payment_type'],
            city=validated_data['city']
        )

        for order_item_data in order_items_data:
            variation = ProductVariation.objects.get(id=order_item_data['variation'])
            OrderItem.objects.create(order=order, variation=variation, quantity=order_item_data['quantity'])
        
        for recommend_product_data in recommend_products_data:
            recommend_product = RecommendProduct.objects.get(id=recommend_product_data['product'])
            OrderItem.objects.create(
                order=order, recommend_product=recommend_product, quantity=recommend_product_data['quantity']
            )

        if validated_data['payment_type'] == 'payu':
            token_url = "https://secure.payu.com/pl/standard/user/oauth/authorize"
            token_headers = {
                "Content-Type": "application/x-www-form-urlencoded"
            }
            token_data = {
                "grant_type": "client_credentials",
                "client_id": settings.PAYU_CLIENT_ID,
                "client_secret": settings.PAYU_CLIENT_SECRET
            }
            token_response = requests.post(token_url, data=token_data, headers=token_headers)

            if token_response.status_code != 200:
                raise serializers.ValidationError("Failed to obtain access token")

            access_token = token_response.json().get("access_token")

            payu_url = "https://secure.payu.com/api/v2_1/orders"
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {access_token}"
            }
            payload = {
                "notifyUrl": f"http://127.0.0.1:8000/orders/{order.id}",
                "continueUrl": f"http://127.0.0.1:8000/orders/{order.id}/success",
                "failureUrl": f"http://127.0.0.1:8000/orders/{order.id}/failed/",
                "customerIp": "127.0.0.1",
                "merchantPosId": settings.PAYU_MERCHANT_POS_ID,
                "description": f"Order {order.id}",
                "currencyCode": "PLN",
                "totalAmount": int(total_amount * 100),
                "buyer": {
                    "email": order.email,
                    "phone": order.phone_num,
                    "firstName": order.first_name,
                    "lastName": order.last_name,
                    "language": "pl",
                    "delivery": {
                        "street": f"{order.address} {order.house_number}",
                        "postalCode": order.postal_code,
                        "city": order.city,
                        "recipientName": f"{order.first_name} {order.last_name}",
                        "recipientEmail": order.email,
                        "recipientPhone": order.phone_num
                    }
                },
                "products": products_payload
            }

            response = requests.post(payu_url, json=payload, headers=headers, allow_redirects=False)


            if response.status_code == 302:
                response_data = response.json()

                if 'redirectUri' in response_data:
                    order.payment_url = response_data['redirectUri']
                    order.save()
            else:
                raise serializers.ValidationError("Payment initialization failed.")

        return order


