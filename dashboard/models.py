from django.db import models

# Create your models here.
class Gifts(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    count = models.IntegerField(default=1)

    def __str__(self):
        return self.name
    
class Order(models.Model):
    gift = models.ForeignKey(Gifts, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    is_viewed = models.BooleanField(default=False)

    def __str__(self):
        return f"Order {self.id} for {self.gift.name}"