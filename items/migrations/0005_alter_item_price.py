# Generated by Django 4.1.7 on 2023-02-21 09:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0004_alter_item_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='price',
            field=models.IntegerField(default=0),
        ),
    ]