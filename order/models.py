from django.db import models

# Create your models here.
class Order_item(models.Model):
    product       = models.ForeignKey('product.Product', on_delete=models.SET_NULL, null=True)
    order_info    = models.ForeignKey('Order', on_delete=models.CASCADE)
    quantity      = models.PositiveIntegerField(default=0)
    price         = models.CharField(max_length=45)
    option        = models.ForeignKey('product.Option', on_delete=models.SET_NULL, null=True)
    delivery_cost = models.ForeignKey('Delivery_cost', on_delete=models.SET_NULL, null=True)
    
    class Meta:
        db_table = 'order_items'

class Order(models.Model):
    user           = models.ForeignKey('user.User', on_delete=models.SET_NULL, null=True) 
    address        = models.ForeignKey('user.Address', on_delete=models.SET_NULL, null=True)
    point          = models.CharField(max_length=45)
    card           = models.ForeignKey('user.Card', on_delete=models.SET_NULL, null=True)
    state          = models.ForeignKey('Order_state', on_delete=models.SET_NULL, null=True)
    memo           = models.CharField(max_length=100, null=True) 
    order_date     = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=45)
    payment_type   = models.IntegerField(default=0)

    class Meta:
        db_table = 'orders'

class Order_state(models.Model):
    state = models.CharField(max_length=45)

    class Meta:
        db_table = 'order_states'

class Delivery_type(models.Model):
    delivery_type = models.CharField(max_length=45)

    class Meta:
        db_table = 'delivery_types'

class Delivery_cost(models.Model):
    delivery_type   = models.ForeignKey('Delivery_type', on_delete=models.CASCADE)
    delivery_method = models.CharField(max_length=45)

    class Meta:
        db_table = 'delivery_costs'