# Generated by Django 3.1.4 on 2021-01-19 04:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0003_auto_20210115_0802'),
    ]

    operations = [
        migrations.AlterField(
            model_name='option',
            name='product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='option', to='product.product'),
        ),
    ]
