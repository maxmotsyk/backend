# Generated by Django 4.2.1 on 2024-06-30 14:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_orderitem_recommend_product_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='Created At'),
        ),
        migrations.AddField(
            model_name='order',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, null=True, verbose_name='Updated At'),
        ),
    ]
