from django.db import models

# Create your models here.
class Category(models.Model):
    category = models.CharField(max_length=45)

    class Meta:
        db_table = 'categories'

class Product(models.Model):
    category    = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True)
    name        = models.CharField(max_length=60)
    price       = models.DecimalField(max_digits=18, decimal_places=2)
    description = models.CharField(max_length=2000)
    pub_date    = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'products'

class Image(models.Model):
    product   = models.ForeignKey('Product', on_delete=models.CASCADE)
    image_url = models.URLField(max_length=2000)
    class Meta:
        db_table = 'images'

class Option(models.Model):
    product = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True)
    name    = models.CharField(max_length=45)
    price   = models.DecimalField(max_digits=18, decimal_places=2, null=True)

    class Meta:
        db_table = 'options'

class Question(models.Model):
    user        = models.ForeignKey('user.User', on_delete=models.CASCADE)
    product     = models.ForeignKey('product.Product', on_delete=models.CASCADE)
    title       = models.CharField(max_length=45)
    content     = models.TextField(max_length=4000)
    image_url   = models.URLField(max_length=2000, null=True)
    secret      = models.BooleanField(default=False)
    secret_code = models.CharField(max_length=45, null=True)
    pub_date    = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'questions'

class Review(models.Model):
    user      = models.ForeignKey('user.User', on_delete=models.CASCADE)
    product   = models.ForeignKey('product.Product', on_delete=models.CASCADE)
    content   = models.TextField(max_length=4000)
    image_url = models.URLField(max_length=2000, null=True)
    pub_date  = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'reviews'

class Comment(models.Model):
    user      = models.ForeignKey('user.User', on_delete=models.CASCADE)
    review    = models.ForeignKey('Review', on_delete=models.CASCADE)
    content   = models.CharField(max_length=2000)
    image_url = models.URLField(max_length=2000, null=True)
    pub_date  = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'comments'