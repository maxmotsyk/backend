# Generated by Django 4.2.1 on 2024-06-22 22:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0003_remove_review_creator_img_remove_review_reviews_img'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='creator_img',
            field=models.FileField(default=None, upload_to='creator_img/', verbose_name='Creator img'),
        ),
        migrations.AddField(
            model_name='review',
            name='reviews_img',
            field=models.FileField(default=None, upload_to='reviews_img/', verbose_name='Reviews img'),
        ),
    ]