from django.db import models
from products.models import Product, ProductVariation, RecommendProduct


class DeliveryMethod(models.Model):
    name = models.CharField(max_length=255, verbose_name="Delivery Method Name")
    description = models.TextField(verbose_name="Description")
    price = models.FloatField(verbose_name="Price")
    img = models.FileField(verbose_name="img", upload_to='deliveru_methods', default=None)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Delivery Method"
        verbose_name_plural = "Delivery Methods"


class Order(models.Model):
    STATUS_CHOICES = [
        ('new', 'New'),
        ('success', 'Success'),
        ('failed', 'Failed'),
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Product")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, verbose_name="Status")
    first_name = models.CharField(max_length=255, verbose_name="First Name")
    last_name = models.CharField(max_length=255, verbose_name="Last Name")
    phone_num = models.CharField(max_length=20, verbose_name="Phone Number")
    email = models.EmailField(verbose_name="Email")
    delivery_method = models.ForeignKey(DeliveryMethod, on_delete=models.CASCADE, verbose_name="Delivery Method")
    address = models.TextField(verbose_name="Address")
    house_number = models.CharField(max_length=20, verbose_name="House Number")
    postal_code = models.CharField(max_length=10, verbose_name="Postal Code")
    city = models.CharField(max_length=255, verbose_name="City")
    total_amount = models.FloatField(verbose_name="Total Amount")

    def __str__(self):
        return f"Order {self.id}"

    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name="Order")
    variation = models.ForeignKey(
        ProductVariation, on_delete=models.CASCADE, verbose_name="Product Variation", blank=True, null=True
    )
    recommend_product = models.ForeignKey(
        RecommendProduct, on_delete=models.CASCADE, verbose_name="Recomend Product", blank=True, null=True
    )
    quantity = models.IntegerField(verbose_name="Quantity")

    def __str__(self):
        return f"OrderItem {self.id}"

    class Meta:
        verbose_name = "Order Item"
        verbose_name_plural = "Order Items"
