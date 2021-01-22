from django.db import models

# Create your models here.
class OrderItem(models.Model):
    product       = models.ForeignKey('product.Product', on_delete=models.SET_NULL, null=True)
    order         = models.ForeignKey('Order', on_delete=models.CASCADE, related_name='orderItem')
    quantity      = models.PositiveIntegerField(default=0)
    price         = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    option        = models.JSONField(null=True)
    delivery_cost = models.ForeignKey('DeliveryCost', on_delete=models.SET_NULL, null=True)
    
    class Meta:
        db_table = 'order_items'

class Order(models.Model):
    user           = models.ForeignKey('user.User', on_delete=models.SET_NULL, null=True, related_name='order') 
    address        = models.ForeignKey('user.Address', on_delete=models.SET_NULL, null=True)
    point          = models.IntegerField(null=True)
    card           = models.ForeignKey('user.Card', on_delete=models.SET_NULL, null=True)
    state          = models.ForeignKey('OrderState', on_delete=models.SET_NULL, null=True)
    memo           = models.CharField(max_length=200, null=True) 
    order_date     = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=45, null=True)
    payment_type   = models.ForeignKey('PaymentType', on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = 'orders'

class PaymentType(models.Model):
    payment_type = models.BooleanField(default=False)

    class Meta:
        db_table = 'payment_types'

class OrderState(models.Model):
    state = models.CharField(max_length=45)

    class Meta:
        db_table = 'order_states'

class DeliveryType(models.Model):
    delivery_type = models.CharField(max_length=45)

    class Meta:
        db_table = 'delivery_types'

class DeliveryCost(models.Model):
    delivery_type   = models.ForeignKey('DeliveryType', on_delete=models.CASCADE)
    delivery_method = models.CharField(max_length=45)

    class Meta:
        db_table = 'delivery_costs'