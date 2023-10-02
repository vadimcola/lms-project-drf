# Generated by Django 4.2.4 on 2023-10-02 07:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('learn', '0004_alter_payments_payment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payments',
            name='payment',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Сумма оплаты'),
        ),
        migrations.AlterField(
            model_name='payments',
            name='payment_method',
            field=models.CharField(blank=True, choices=[('cash', 'Наличные'), ('account', 'Оплата на счет'), ('card', 'Оплата банковской картой')], max_length=7, null=True, verbose_name='Метод оплаты'),
        ),
    ]