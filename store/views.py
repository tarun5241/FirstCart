from django.shortcuts import render,get_object_or_404
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

from carts.models import CartItem
from carts.views import _cart_id
from category.models import Category
from store.models import Product


def store(request, category_slug=None):
    categories = None
    products = None
    
    if category_slug != None:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=categories, is_available=True).order_by('id')
        
        # Pagination Code
        paginator = Paginator(products, 6)
        page =  request.GET.get('page')
        paged_products = paginator.get_page(page)
        
        # Count of products in database
        products_count = products.count()
    else:
        products = Product.objects.all().filter(is_available=True).order_by('id')
        
        # Pagination Code
        paginator = Paginator(products, 3)
        page =  request.GET.get('page')
        paged_products = paginator.get_page(page)
        
        # Count of products in database
        products_count = products.count()
        # categories = Category.objects.all()
    context = {
        'products':paged_products,
        'products_count':products_count,
        # 'categories':categories,
    }
    return render(request, 'store/store.html', context)


def product_detail(request, category_slug, product_slug):
    try:
        product = Product.objects.get(category__slug=category_slug, slug=product_slug)
        in_cart = CartItem.objects.filter(cart__cart_id = _cart_id(request),product=product).exists()
        
    except Exception as e:
        raise e
    context = {
        'product':product,
        'in_cart':in_cart,
    }
    return render(request, 'store/product-detail.html',context)