# Generated by Django 2.1.1 on 2021-08-12 23:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordermodel',
            name='balance',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='ordermodel',
            name='contact',
            field=models.CharField(max_length=24),
        ),
        migrations.AlterField(
            model_name='ordermodel',
            name='created',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='ordermodel',
            name='days',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='ordermodel',
            name='deposit',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='ordermodel',
            name='price',
            field=models.CharField(max_length=100),
        ),
    ]
