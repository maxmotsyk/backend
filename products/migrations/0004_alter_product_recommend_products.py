# Generated by Django 4.2.1 on 2024-07-08 16:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_productvariation_img'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='recommend_products',
            field=models.ManyToManyField(related_name='recommended_for', to='products.recommendproduct', verbose_name='Recommended Products'),
        ),
    ]
