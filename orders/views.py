from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.db import transaction
from .models import Order, OrderedItem, Cart
from products.models import Product


def show_cart(request):
    user = request.user
    # print(request.user.customer_profile.phoneno,user.customer_profile)
    cart_obj = Cart.objects.filter(cart_onwer=user.customer_profile)
    # print(cart_obj)
    return render(request,'cart.html',{'cart':cart_obj})


def add_to_cart(request):
    if request.method =='POST':
        user = request.user
        customer = user.customer_profile
        quantity = int(request.POST.get('quantity'))
        product_id = request.POST.get('product_id')
        product = Product.objects.get(pk=product_id)

        cart_obj, created = Cart.objects.get_or_create(
            cart_onwer = customer,
            product = product,
        )
        if created:
            print('new')
            cart_obj.quantity = quantity
            cart_obj.save()

        else:
            print('add')
            cart_obj.quantity += quantity
            cart_obj.save()
        # ordered_item, created = OrderedItem.objects.get_or_create(
        #     product = product,
        #     owner = cart_obj,
        # )
        # if created:
        #     ordered_item.quantity = quantity
        #     ordered_item.save()

        # else:
        #     ordered_item.quantity += quantity
        #     ordered_item.save()
        # print('items',ordered_item)

    return redirect('cart')
    # return render(request,'cart.html',{'cart':cart_obj})



def remove_item(request, pk):
    try:
        item = Cart.objects.get(pk=pk)
        if item.quantity > 1:
            item.quantity -= 1
            item.save()
        else:
            item.delete()
    except Cart.DoesNotExist:
        pass
    return redirect('cart')

def make_payment(request,pk):
    ordered_obj = Order.objects.get(pk=pk)
    if ordered_obj:
        ordered_obj.order_status = 'ORDER_PLACED'
        ordered_obj.save()

        subject = "Order Confirmed"
        message = "Your payment for the order has been successfully processed. Your Order is on its way."
        sender_email = settings.EMAIL_HOST_USER
        customer_email = ordered_obj.owner.user.email
        send_mail(subject, message, sender_email, [customer_email])
    return redirect('cart')



def place_order(request):
    customer = request.user.customer_profile
    cart_items = Cart.objects.filter(cart_onwer=customer)

    total = 0
    for item in cart_items:
        total += item.quantity * item.product.price

    order_obj = Order.objects.create(owner=customer, total_price=total)
    order_obj.address = customer.address
    order_obj.save()
    ordered_items = []
    for item in cart_items:
        ordered_items.append(OrderedItem(
            product=item.product,
            quantity=item.quantity,
            owner=order_obj
        ))
    OrderedItem.objects.bulk_create(ordered_items)
    cart_items.delete()

    return render(request, 'payment.html', {'total': total, 'order_obj': order_obj})


def view_orders(request):
    user = request.user
    customer = user.customer_profile
    orders = Order.objects.filter(owner=customer).exclude(order_status=Order.CART_STAGE)
    print('orders',orders)
    return render(request, 'order.html',{'orders':orders})


def view_order_details(request,pk):
    order = get_object_or_404(Order, pk=pk)
    ordered_items = OrderedItem.objects.filter(owner=order)
    return render(request, 'orderdetails.html', {'ordered_items': ordered_items})

