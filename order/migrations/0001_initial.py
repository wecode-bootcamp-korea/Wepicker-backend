# Generated by Django 3.1.4 on 2021-01-13 01:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('product', '0002_auto_20210113_0136'),
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Delivery_cost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('delivery_method', models.CharField(max_length=45)),
            ],
            options={
                'db_table': 'delivery_costs',
            },
        ),
        migrations.CreateModel(
            name='Delivery_type',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('delivery_type', models.CharField(max_length=45)),
            ],
            options={
                'db_table': 'delivery_types',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('point', models.CharField(max_length=45)),
                ('memo', models.CharField(max_length=100, null=True)),
                ('order_date', models.DateTimeField(auto_now_add=True)),
                ('payment_method', models.CharField(max_length=45)),
                ('payment_type', models.IntegerField(default=0)),
                ('address', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='user.address')),
                ('card', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='user.card')),
            ],
            options={
                'db_table': 'orders',
            },
        ),
        migrations.CreateModel(
            name='Order_state',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('state', models.CharField(max_length=45)),
            ],
            options={
                'db_table': 'order_states',
            },
        ),
        migrations.CreateModel(
            name='Order_item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=0)),
                ('price', models.CharField(max_length=45)),
                ('delivery_cost', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='order.delivery_cost')),
                ('option', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='product.option')),
                ('order_info', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='order.order')),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='product.product')),
            ],
            options={
                'db_table': 'order_items',
            },
        ),
        migrations.AddField(
            model_name='order',
            name='state',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='order.order_state'),
        ),
        migrations.AddField(
            model_name='order',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='user.user'),
        ),
        migrations.AddField(
            model_name='delivery_cost',
            name='delivery_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='order.delivery_type'),
        ),
    ]
