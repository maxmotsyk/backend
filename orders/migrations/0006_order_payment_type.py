# Generated by Django 4.2.1 on 2024-07-06 14:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0005_order_payment_url_alter_orderitem_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='payment_type',
            field=models.CharField(choices=[('payu', 'Pay U'), ('payment_on_delivery', 'Payment on delivery')], max_length=20, null=True, verbose_name='Payment Type'),
        ),
    ]
