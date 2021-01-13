from django.db import models

class User(models.Model):
    userId         = models.CharField(max_length=50)
    password       = models.CharField(max_length=1000)
    name           = models.CharField(max_length=50)
    phone          = models.CharField(max_length=50)
    email          = models.EmailField(max_length=120, null=True)
    profile_photo  = models.CharField(max_length=1000, null=True)

    class Meta:
        db_table = 'users'

class Point(models.Model):
    user         = models.ForeignKey('User', on_delete=models.CASCADE)
    content      = models.CharField(max_length=80)
    point        = models.CharField(max_length=45)
    payment_date = models.DateTimeField(auto_now_add=True)

    class Mete:
        db_table = 'points'

class Card(models.Model):
    user        = models.ForeignKey('User', on_delete=models.CASCADE)
    company     = models.CharField(max_length=45)
    number      = models.CharField(max_length=45)
    expire_date = models.DateTimeField(auto_now_add=True)

    class Mets:
        db_table = 'cards'

class Address(models.Model):
    user        = models.ForeignKey('User', on_delete=models.CASCADE) 
    address     = models.CharField(max_length=400)
    post_number = models.CharField(max_length=45)
    default     = models.IntegerField(default=0)

    class Mete:
        db_table = 'addresses'

class Wish_list(models.Model):
    user    = models.ForeignKey('User', on_delete=models.CASCADE) 
    product = models.ForeignKey('product.Product', on_delete=models.CASCADE)

    class Meta:
        db_table = 'wish_lists'

class Personal_question(models.Model):
    user      = models.ForeignKey('User', on_delete=models.CASCADE)
    title     = models.CharField(max_length=45)
    content   = models.TextField(max_length=3000)
    image_url = models.CharField(max_length=1000, null=True)
    secret    = models.PositiveIntegerField(default=0)
    pub_date  = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'personal_questions'

