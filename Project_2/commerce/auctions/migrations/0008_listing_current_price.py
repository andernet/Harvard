# Generated by Django 3.1.1 on 2020-10-03 17:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0007_remove_listing_current_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='current_price',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
    ]
