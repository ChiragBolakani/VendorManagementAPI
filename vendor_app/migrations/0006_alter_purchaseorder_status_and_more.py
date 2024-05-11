# Generated by Django 4.2.11 on 2024-05-04 17:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendor_app', '0005_alter_purchaseorder_status_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchaseorder',
            name='status',
            field=models.CharField(choices=[('P', 'Pending'), ('CL', 'Cancelled'), ('CP', 'Completed')], default='P', max_length=2),
        ),
        migrations.AlterField(
            model_name='vendor',
            name='quality_rating_avg',
            field=models.FloatField(default=0.0),
        ),
    ]
