from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Product, Category

# Create your views here.
def catalog(request):
    q = request.GET.get('q', '').strip() #ottengo la stringa scritta nel form
    cat_id = request.GET.get('cat', '')

    products = Product.objects.all().order_by('-id')
    if q:
        products = products.filter( Q(name__icontains=q) | Q(description__icontains=q))

    if cat_id and cat_id.isdigit():
        products = products.filter(category_id=int(cat_id))

    page_obj = Paginator(products.order_by("-id"), 25).get_page(request.GET.get('page'))

    context = { #dizionario per filtrare in base a ricerca nella barra + categoria
        'page_obj': page_obj,
        'q': q,
        'cat': cat_id,
        'categories': Category.objects.all(),
    }

    return render(request, "store/catalog_and_search.html",context)
