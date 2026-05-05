from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, CartItem, Order

def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products': products})


def product(request, pk):
    product = get_object_or_404(Product, id=pk)
    return render(request, 'product.html', {'product': product})


def add_to_cart(request, pk):
    product = get_object_or_404(Product, id=pk)
    item, created = CartItem.objects.get_or_create(product=product)
    
    if not created:
        item.quantity += 1
        item.save()

    return redirect('cart')


def cart_view(request):
    items = CartItem.objects.all()
    total = sum(item.total_price() for item in items)

    return render(request, 'cart.html', {
        'items': items,
        'total': total
    })


def remove_from_cart(request, pk):
    item = get_object_or_404(CartItem, id=pk)
    item.delete()
    return redirect('cart')


def checkout(request):
    CartItem.objects.all().delete()
    Order.objects.create()
    return render(request, 'cart.html', {'message': 'Order placed successfully!'})