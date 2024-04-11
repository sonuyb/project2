from django.db import models
from products.models import Product
from customers.models import Customer

# class OrderStatus:
#     ORDER_PLACED = 'ORDER_PLACED'
#     ORDER_PROCESSED = 'ORDER_PROCESSED'
#     ORDER_DELIVERED = 'ORDER_DELIVERED'
#     ORDER_REJECTED = 'ORDER_REJECTED'

class Cart(models.Model):
    product = models.ForeignKey(Product,related_name='carts',on_delete=models.SET_NULL,null=True)
    quantity = models.IntegerField(default=1)
    cart_onwer = models.ForeignKey(Customer, on_delete=models.SET_NULL,null=True)


class Order(models.Model):
    LIVE = 1
    DELETE = 0
    DELETE_CHOICES = ((LIVE,'LIVE'),
                      (DELETE,'DELETE'))
    CART_STAGE = 0
    # ORDER_CONFIRMED = 1
    # ORDER_PROCESSED = 2
    # ORDER_DELIVERED = 3
    # ORDER_REJECTED = 4
    STATUS_CHOICE = (('ORDER_PLACED','ORDER_PLACED'),
                    ('ORDER_PROCESSED','ORDER_PROCESSED'),
                     ('ORDER_DELIVERED','ORDER_DELIVERED'),
                     ('ORDER_REJECTED','ORDER_REJECTED'))
    order_status = models.CharField(choices=STATUS_CHOICE,max_length=20,null=True,blank=True)
    # order_status = models.IntegerField(choices=STATUS_CHOICE,default=LIVE)
    # order_status = models.CharField(choices=STATUS_CHOICE,max_length=20,default='ORDER_CONFIRMED')
    owner = models.ForeignKey(Customer, on_delete=models.SET_NULL,null=True,related_name='orders')
    total_price = models.FloatField(default=0)
    delete_status = models.IntegerField(choices=DELETE_CHOICES,default=LIVE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class OrderedItem(models.Model):
    product = models.ForeignKey(Product,related_name='added_carts',on_delete=models.SET_NULL,null=True)
    quantity = models.IntegerField(default=1)
    owner = models.ForeignKey(Order, on_delete=models.CASCADE)
    # order = models.ForeignKey(Order, on_delete=models.CASCADE,related_name='added_items')

