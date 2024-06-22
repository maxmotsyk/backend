from django.db import models
from products.models import Product


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Product")
    message = models.TextField(verbose_name="Message")
    rating_stars = models.PositiveSmallIntegerField(verbose_name="Rating Stars")
    created_by = models.CharField(max_length=255, verbose_name="Created By")
    reviews_img = models.FileField(verbose_name="Reviews img", upload_to='reviews_img/', default=None, blank=True, null=True)
    creator_img = models.FileField(verbose_name="Creator img", upload_to='creator_img/', default=None, blank=True, null=True)

    def __str__(self):
        return self.message

    class Meta:
        verbose_name = "Review"
        verbose_name_plural = "Reviews"
