# Generated by Django 3.1.4 on 2021-01-13 06:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user', '0001_initial'),
        ('product', '0002_auto_20210113_0614'),
    ]

    operations = [
        migrations.CreateModel(
            name='DeliveryCost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('delivery_method', models.CharField(max_length=45)),
            ],
            options={
                'db_table': 'delivery_costs',
            },
        ),
        migrations.CreateModel(
            name='DeliveryType',
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
                ('point', models.IntegerField()),
                ('memo', models.CharField(max_length=200, null=True)),
                ('order_date', models.DateTimeField(auto_now_add=True)),
                ('payment_method', models.CharField(max_length=45)),
                ('address', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='user.address')),
                ('card', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='user.card')),
            ],
            options={
                'db_table': 'orders',
            },
        ),
        migrations.CreateModel(
            name='OrderState',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('state', models.CharField(max_length=45)),
            ],
            options={
                'db_table': 'order_states',
            },
        ),
        migrations.CreateModel(
            name='PaymentType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_type', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'payment_types',
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=0)),
                ('price', models.DecimalField(decimal_places=2, max_digits=18)),
                ('delivery_cost', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='order.deliverycost')),
                ('option', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='product.option')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='order.order')),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='product.product')),
            ],
            options={
                'db_table': 'order_items',
            },
        ),
        migrations.AddField(
            model_name='order',
            name='payment_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='order.paymenttype'),
        ),
        migrations.AddField(
            model_name='order',
            name='state',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='order.orderstate'),
        ),
        migrations.AddField(
            model_name='order',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='user.user'),
        ),
        migrations.AddField(
            model_name='deliverycost',
            name='delivery_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='order.deliverytype'),
        ),
    ]
