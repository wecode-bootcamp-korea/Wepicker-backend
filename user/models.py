from django.db              import models

class User(models.Model):
    account        = models.CharField(max_length=50)
    password       = models.CharField(max_length=1000)
    name           = models.CharField(max_length=50)
    phone          = models.CharField(max_length=50)
    email          = models.EmailField(max_length=120)
    profile_photo  = models.URLField(max_length=2000, null=True)

    class Meta:
        db_table = 'users'

class Point(models.Model):
    user         = models.ForeignKey('User', on_delete=models.CASCADE, related_name='point')
    content      = models.CharField(max_length=80)
    point        = models.IntegerField()
    payment_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'points'

class Card(models.Model):
    user          = models.ForeignKey('User', on_delete=models.CASCADE, related_name='card')
    company       = models.CharField(max_length=45)
    number        = models.CharField(max_length=45)
    expired_year  = models.CharField(max_length=45, default='')
    expired_month = models.CharField(max_length=45, default='')

    class Meta:
        db_table = 'cards'

class Address(models.Model):
    user        = models.ForeignKey('User', on_delete=models.CASCADE, related_name='address') 
    address     = models.CharField(max_length=400)
    post_number = models.CharField(max_length=45)
    default     = models.BooleanField(default=False)

    class Meta:
        db_table = 'addresses'

class WishList(models.Model):
    user    = models.ForeignKey('User', on_delete=models.CASCADE) 
    product = models.ForeignKey('product.Product', on_delete=models.CASCADE)

    class Meta:
        db_table = 'wish_lists'


