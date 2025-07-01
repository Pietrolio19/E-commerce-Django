from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.db.models import Q
from .models import *

# Create your views here.
def catalog(request):
    q = request.GET.get('q', '').strip()
    cat_id = request.GET.get('cat', '')

    products = Product.objects.all().order_by('-id')
    if q:
        products = products.filter( Q(name__icontains=q) | Q(description__icontains=q))

    if cat_id and cat_id.isdigit():
        products = products.filter(Q(category_id=int(cat_id)) | Q(related_category__id=int(cat_id))).distinct()

    page_obj = Paginator(products.order_by("-id"), 25).get_page(request.GET.get('page'))

    context = { #dizionario per filtrare in base a ricerca nella barra + categoria
        'page_obj': page_obj,
        'q': q,
        'cat': cat_id,
        'categories': Category.objects.all(),
    }

    return render(request, "store/catalog_and_search.html",context)

def cart_view(request):
    user_filter = request.user if request.user.is_authenticated else None
    order = Order.objects.filter(user=user_filter, status="in_progress").prefetch_related("items__product").first()
    return render(request, "store/cart.html", {'order': order})

def add_to_cart(request, product_id, qty=1):
    product = get_object_or_404(Product, pk=product_id)

    user_ref = request.user if request.user.is_authenticated else None

    #in caso l'utente non abbia ancora un ordine in sospeso ne creo uno
    order, _ = Order.objects.get_or_create(user=user_ref, status="in_progress")

    item, created = OrderItem.objects.get_or_create(order=order, product=product, defaults= {'quantity': qty})

    if not created:
        item.quantity += qty
        item.save()

    return redirect("cart_view")

def remove_from_cart(request, product_id):
    user_ref = request.user if request.user.is_authenticated else None
    item = get_object_or_404(OrderItem, pk=product_id, order__user=user_ref, order__status="in_progress")
    item.delete()
    return redirect("cart_view")
