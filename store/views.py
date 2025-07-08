from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import messages
from accounts.models import CustomUser
from .models import *

# Create your views here.
def catalog(request):
    user = request.user
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
        'user': user,
    }

    return render(request, "store/catalog_and_search.html",context)

@login_required(login_url='/login/')
def cart_view(request):
    user_filter = request.user if request.user.is_authenticated else None
    order = Order.objects.filter(user=user_filter, status="in_progress").prefetch_related("items__product").first()
    categories = Category.objects.all()
    return render(request, "store/cart.html", {'order': order, 'categories': categories})

@login_required(login_url="/login/")
def add_to_cart(request, product_id, qty=1):
    product = get_object_or_404(Product, pk=product_id)

    user_ref = request.user if request.user.is_authenticated else None

    if not product.available:
        context = {
            'product': product,
            'error_message': 'Il prodotto selezionato non è attualmente disponibile.'
        }
        return render(request, 'store/product_error.html', context)

    #in caso l'utente non abbia ancora un ordine in sospeso ne creo uno
    order, _ = Order.objects.get_or_create(user=user_ref, status="in_progress")

    item, created = OrderItem.objects.get_or_create(order=order, product=product, defaults= {'quantity': qty})

    if not created:
        item.quantity += qty
        item.save()

    messages.success(request, f'{product.name} è stato aggiunto al carrello.')
    return redirect("cart_view")

@login_required(login_url="/login/")
def remove_from_cart(request, product_id):
    user_ref = request.user if request.user.is_authenticated else None
    item = get_object_or_404(OrderItem, pk=product_id, order__user=user_ref, order__status="in_progress")
    item.delete()
    return redirect("cart_view")

@login_required
def checkout(request):
    order = Order.objects.filter(
        user=request.user,
        status="in_progress"
    ).prefetch_related("items__product").first()

    if not order or order.items.count() == 0:
        messages.error(request, "Il tuo carrello è vuoto.")
        return redirect('catalog')

    payment_method = ''
    shipping_address = ''
    addresses = CustomUser.objects.filter(pk=request.user.pk).values_list("address", flat=True)
    categories = Category.objects.all()

    if request.method == 'POST':
        payment_method = request.POST.get('payment_method')
        shipping_address = request.POST.get('shipping_address')

        if not payment_method or not shipping_address:
            messages.error(request, "Metodo di pagamento e indirizzo sono obbligatori.")
            return redirect('checkout')

        order.payment_method = payment_method
        order.shipping_address = shipping_address
        order.save()

        messages.success(request, "Ordine confermato con successo!")
        return redirect('checkout')

    context = {
        'order': order,
        'addresses': addresses,
        'categories': categories,
        'payment_method': payment_method,
        'shipping_address': shipping_address,
    }

    return render(request, "store/checkout.html", context)

@login_required(login_url="/login/")
def payment(request):
    current_order = get_object_or_404(Order, user=request.user, status="in elaborazione")
    current_order.status = "completato"
    items = current_order.items.all()
    for o in items:
        o.product.stock -= o.quantity
        o.product.save()
    current_order.save()
    return render(request, "store/payment.html")
