# Generated by Django 4.2.1 on 2024-06-22 21:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_remove_product_img_productimage'),
    ]

    operations = [
        migrations.AddField(
            model_name='productvariation',
            name='img',
            field=models.FileField(default=None, upload_to='product_variation/', verbose_name='img'),
        ),
    ]