from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator
from .models import Product

# Create your views here.
def catalog(request):
    products = Product.objects.all().order_by('-id')
    page_obj = Paginator(products, 24).get_page(request.GET.get('page'))
    return render(request, "store/catalog_and_search.html", {'page_obj': page_obj})
