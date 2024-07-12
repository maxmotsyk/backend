from django.db import models


class RecommendProduct(models.Model):
    name = models.CharField(max_length=255, verbose_name="Name")
    description = models.TextField(verbose_name="Description")
    price = models.FloatField(verbose_name="Price")
    img = models.FileField(verbose_name="Img", upload_to="rcomend_products/")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Recommended Product"
        verbose_name_plural = "Recommended Products"


class Product(models.Model):
    title = models.CharField(max_length=255, verbose_name="Title")
    description = models.TextField(verbose_name="Description")
    price = models.FloatField(verbose_name="Price")
    discount = models.IntegerField(verbose_name="Discount")
    recommend_products = models.ManyToManyField(RecommendProduct, verbose_name="Recommended Products", related_name='recommended_for')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images', verbose_name="Product")
    image = models.FileField(upload_to='product_images/', verbose_name="Image")

    def __str__(self):
        return f"Image for {self.product.title}"

    class Meta:
        verbose_name = "Product Image"
        verbose_name_plural = "Product Images"


class ProductDetail(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Product")
    icon = models.ImageField(upload_to='product_icons/', verbose_name="Icon")
    name = models.CharField(max_length=255, verbose_name="Name")
    description = models.TextField(verbose_name="Description")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Product Detail"
        verbose_name_plural = "Product Details"


class ProductVariation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Product")
    description = models.TextField(verbose_name="Description")
    img = models.FileField(verbose_name="img", upload_to='product_variation/', default=None)

    def __str__(self):
        return self.description

    class Meta:
        verbose_name = "Product Variation"
        verbose_name_plural = "Product Variations"
