from django.db import models
from PPM_project import settings


# Create your models here.
class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='in_progress')

    def total_order_cost(self):
        return sum(item.total_cost() for item in self.items.all())

    def __str__(self):
        return f'{self.user.username} - {self.status}'

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    available = models.BooleanField(default=True)
    stock = models.PositiveIntegerField()
    category = models.ForeignKey("Category", on_delete=models.CASCADE)

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