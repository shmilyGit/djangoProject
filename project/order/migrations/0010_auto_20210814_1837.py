# Generated by Django 2.1.1 on 2021-08-14 18:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0009_auto_20210814_1740'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ordermodel',
            old_name='days',
            new_name='effectdays',
        ),
    ]
