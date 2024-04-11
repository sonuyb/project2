from django.shortcuts import render, redirect
from. forms import AddProducts
from products. models import Product
from orders . models import Order


def admin_dash(request):
    return render(request,'admin/admindash.html')

def products(request):
    return render(request,'admin/products.html')

def add_products(request):
    if request.method == 'POST':
        form = AddProducts(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('products')
        else:
            print(form.errors)
    else:
        form = AddProducts()
    return render(request,'admin/addproducts.html',{'form':form})


def view_products(request):
    products = Product.objects.all()
    return render(request,'admin/viewproducts.html',{'products':products})


def edit(request,pk):
    instance_edit = Product.objects.get(pk=pk)
    if request.POST:
        form = AddProducts(request.POST, instance=instance_edit)
        if form.is_valid():
            instance_edit.save()
            return view_products(request)
    else:
        form = AddProducts(instance=instance_edit)
    return render(request,'admin/addproducts.html',{'form':form})


def delete(request,pk):
    instance = Product.objects.get(pk=pk)
    instance.delete()
    return view_products(request)

def view_all_orders(request):
    orders = Order.objects.all()
    return render(request,'admin/view-all-order.html',{'orders':orders})

def update_order_status(request, order_id):
    if request.method == 'POST':
        order = Order.objects.get(id=order_id)
        new_status = request.POST.get('status')

        order.order_status = new_status
        order.save()


        return redirect('allorders')  
    else:
        return redirect('allorders')