# Generated by Django 3.2.9 on 2021-11-11 15:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0002_alter_category_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='rating',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='product',
            name='rating_quantity',
            field=models.IntegerField(default=0),
        ),
    ]