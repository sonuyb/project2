from django.db import models
from customers.models import Customer


class Product(models.Model):
    DELETE_CHOICES = ((0,'DELETE'),
                      (1,'LIVE'))
    CATEGORY_CHOICES = (('men','men'),
                        ('women','women'),
                        ('kid','kid'))
    title = models.CharField(max_length=200)
    price = models.FloatField()
    description = models.TextField()
    image = models.ImageField(upload_to='media/')
    priority = models.IntegerField(default=0)
    category = models.CharField(choices=CATEGORY_CHOICES,max_length=20,null=True,blank=True)
    qunatity = models.IntegerField(default=0)
    delete_status = models.IntegerField(choices=DELETE_CHOICES,default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    

class Review(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.CASCADE)
    item = models.ForeignKey(Product, on_delete=models.CASCADE)
    review_desp = models.CharField(max_length=100)
    rating = models.IntegerField()