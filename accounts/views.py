from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from .mixins import *
from django.urls import reverse_lazy
from django.contrib.auth import login
from django.views.generic import CreateView, DetailView, DeleteView, UpdateView
from store.models import Order, Category, Product
from .forms import SignUpForm, OrderItemFormSet
from .models import CustomUser

# Create your views here.
class SignUpView(CreateView):
    form_class    = SignUpForm
    template_name = "accounts/sign_up.html"
    success_url   = reverse_lazy("catalog")

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response


class CustomLoginView(LoginView):
    template_name = "accounts/login.html"

    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)
        if user.is_store_manager:
            return redirect('accounts:manager')
        else:
            return redirect('catalog')

class ProfileView(LoginRequiredMixin, CustomerRequiredMixin, DetailView):
    model = CustomUser
    template_name = 'accounts/user_info.html'
    context_object_name = 'user_obj'

    def get_object(self):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['orders'] = (
            Order.objects.all().filter(user=self.request.user)
            .select_related('user')
            .prefetch_related('items', 'items__product')
            .order_by('-completed_at')
        )
        context['categories'] = (Category.objects.all())
        return context

class ManagerView(LoginRequiredMixin, StoreManagerMixin, DetailView):
    model = CustomUser
    template_name = 'accounts/manager_control_panel.html'
    context_object_name = 'manager_obj'

    def get_object(self):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['orders'] = (Order.objects.all())
        context['products'] = (Product.objects.all())
        context['categories'] = (Category.objects.all())

        return context

#CRUD view per product

class ProductCreateView(LoginRequiredMixin, StoreManagerMixin, CreateView):
    model = Product
    fields = ['name', 'price', 'stock', 'available', 'category', 'related_category', 'description']
    template_name = 'accounts/product/product_create.html'
    success_url = reverse_lazy('accounts:manager')

class ProductDeleteView(LoginRequiredMixin, StoreManagerMixin, DeleteView):
    model = Product
    template_name = 'accounts/product/product_delete_confirmation.html'
    success_url = reverse_lazy('accounts:manager')

class ProductUpdateView(LoginRequiredMixin, StoreManagerMixin, UpdateView):
    model = Product
    fields = ['name', 'price', 'stock', 'available', 'category', 'related_category', 'description']
    template_name = 'accounts/product/product_update_confirmation.html'
    success_url = reverse_lazy('accounts:manager')

#CRUD view per Category

class CategoryCreateView(LoginRequiredMixin, StoreManagerMixin, CreateView):
    model = Category
    fields = ['name']
    template_name = 'accounts/category/category_create.html'
    success_url = reverse_lazy('accounts:manager')


class CategoryDeleteView(LoginRequiredMixin, StoreManagerMixin, DeleteView):
    model = Category
    template_name = 'accounts/category/category_delete_confirmation.html'
    success_url = reverse_lazy('accounts:manager')

class CategoryUpdateView(LoginRequiredMixin, StoreManagerMixin, UpdateView):
    model = Category
    fields = ['name']
    template_name = 'accounts/category/update_category_confirmation.html'
    success_url = reverse_lazy('accounts:manager')

#CRUD view per Order

class OrderDeleteView(LoginRequiredMixin, StoreManagerMixin, DeleteView):
    model = Order
    template_name = 'accounts/order/delete_order_confirmation.html'
    success_url = reverse_lazy('accounts:manager')

class OrderUpdateView(LoginRequiredMixin, StoreManagerMixin, UpdateView):
    model = Order
    fields = ['user', 'status', 'completed_at', 'payment_method', 'shipping_address']
    template_name = 'accounts/order/update_order_confirmation.html'
    success_url = reverse_lazy('accounts:manager')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['items_formset'] = OrderItemFormSet(self.request.POST, instance=self.object)
        else:
            context['items_formset'] = OrderItemFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        items_formset = context['items_formset']
        if items_formset.is_valid():
            self.object = form.save()
            items_formset.instance = self.object
            items_formset.save()
            return super().form_valid(form)
        else:
            return self.form_invalid(form)