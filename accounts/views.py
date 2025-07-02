from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth import login
from django.views.generic import CreateView
from .forms import SignUpForm

# Create your views here.
class SignUpView(CreateView):
    form_class    = SignUpForm
    template_name = "accounts/sign_up.html"
    success_url   = reverse_lazy("catalog")

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response


class LoginView:
    pass