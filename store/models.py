from django.utils import timezone
from django.db import models
from PPM_project import settings


# Create your models here.
class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='in_progress')
    completed_at = models.DateTimeField(null=True, blank=True)
    payment_method = models.CharField(max_length=100, null=True, blank=True)
    shipping_address = models.TextField(null=True, blank=True)

    def total_order_cost(self):
        return sum(item.total_cost() for item in self.items.all())

    def save(self, *args, **kwargs):
        if self.status == 'completed' and self.completed_at is None:
            self.completed_at = timezone.now()

        super().save(*args, **kwargs)


    def __str__(self):
        if self.status == 'completed':
            order_state = 'completato'
            info = f'Ordine effettuato da {self.user} in data: {self.completed_at:%Y-%m-%d %H:%M}, in stato: {order_state}'
        else:
            order_state = 'in elaborazione'
            info = f'Ordine creato da {self.user} in data: {self.created_at:%Y-%m-%d %H:%M}, stato: {order_state}'
        return info


class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    available = models.BooleanField(default=True)
    stock = models.PositiveIntegerField()
    category = models.ForeignKey("Category", on_delete=models.CASCADE, related_name="products")
    related_category = models.ManyToManyField("Category", blank=True, related_name="_related_products")
    description = models.TextField()

    def set_available(self):
        if self.stock == 0:
            self.available = False

    def __str__(self):
        return f'{self.name}'

class OrderItem(models.Model):
    order = models.ForeignKey("Order", on_delete=models.CASCADE, related_name='items') #per funzione sopra
    product = models.ForeignKey("Product", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def total_cost(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f'{self.product.name} - {self.quantity}'

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.name}'