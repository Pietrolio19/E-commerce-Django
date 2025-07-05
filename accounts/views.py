from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth import login
from django.views.generic import CreateView, DetailView
from store.models import Order, Category
from .forms import SignUpForm
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

class ProfileView(LoginRequiredMixin, DetailView):
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

class ManagerView(LoginRequiredMixin, DetailView):
    model = CustomUser
    template_name = 'accounts/manager_control_panel.html'