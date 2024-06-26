# Generated by Django 4.2.13 on 2024-06-24 11:48

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0002_review_creator_img_review_img'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='rating_stars',
            field=models.PositiveSmallIntegerField(validators=[django.core.validators.MaxValueValidator(5)], verbose_name='Rating Stars'),
        ),
    ]
