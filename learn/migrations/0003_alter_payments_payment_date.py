# Generated by Django 4.2.4 on 2023-09-29 09:44

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('learn', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payments',
            name='payment_date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Дата оплаты'),
        ),
    ]
