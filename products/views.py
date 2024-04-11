from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .models import Product, Review
from customers . models import Customer

def index(request):
    new_arrivals = Product.objects.order_by('-id')[:8]
    featured_products = Product.objects.order_by('priority')[:4]
    name = ''
    if request.user.is_authenticated:
        name = request.user.customer_profile.name
    return render(request,'index.html', {'new_arrivals':new_arrivals,'featured_products':featured_products,'name':name})


def list_products(request):
    page_number = request.GET.get('page', 1)

    products = Product.objects.filter(delete_status=1)
    
    sort_option = request.GET.get('sort')
    if sort_option == '1':
        products = products.order_by('price')
    elif sort_option == '2':
        products = products.order_by('-price')
    query = request.GET.get('query')
    if query:
        products = products.filter(Q(title__icontains=query)|Q(price__icontains=query)|Q(category__icontains=query))
    
    paginator = Paginator(products, 4)
    page_obj = paginator.get_page(page_number)

    return render(request, 'product.html', {'products': page_obj})

@login_required
def product_details(request,pk):
    products = Product.objects.filter(pk=pk)
    # print(products)
    return render(request,'product_details.html',{'products':products})


@login_required
def product_review(request,pk):
    products = get_object_or_404(Product,pk=pk)
    user_detail = request.user.customer_profile
    if request.method == 'POST':
        star_rating = request.POST.get('rating')
        review = request.POST.get('item_review')

        item_reviews = Review.objects.create(user = user_detail,item = products,rating=star_rating,review_desp=review)
        item_reviews.save()

    rating_details = Review.objects.filter(item=products)

    return render(request,'review.html',{'rating_details':rating_details})