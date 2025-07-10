from django import forms
from django.contrib.auth import get_user_model
from django.forms import inlineformset_factory
from store.models import Order, OrderItem

OrderItemFormSet = inlineformset_factory(
    Order,
    OrderItem,
    fields=['product', 'quantity'],
    extra=0,
    can_delete=True
)

User = get_user_model()

class SignUpForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ("username",
                  "email",
                  "name",
                  "surname",
                  "address",
                  "city",
                  "state",
                  "CAP",
                  "is_store_manager")
    widgets = {
    "address": forms.Textarea(attrs={"rows": 2}),
    }

    def clean_password2(self):
        if self.cleaned_data['password1'] != self.cleaned_data['password2']:
            raise forms.ValidationError('Le password non corrispondono')
        return self.cleaned_data['password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()

        return user