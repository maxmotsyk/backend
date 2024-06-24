# Generated by Django 4.2.13 on 2024-06-24 13:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_productvariation_img'),
        ('orders', '0002_deliverymethod_img'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='recommend_product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='products.recommendproduct', verbose_name='Recomend Product'),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='variation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='products.productvariation', verbose_name='Product Variation'),
        ),
    ]