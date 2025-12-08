from django.db import models
import uuid

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
    
class QRCode(models.Model):
    token = models.CharField(max_length=64, unique=True, blank=True)
    qr_image = models.ImageField(upload_to='qr_codes/')
    available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    
    def save(self, *args, **kwargs):
        if not self.token:
            self.token = str(uuid.uuid4())
        super().save(*args, **kwargs)

    def __str__(self):
        return f"QRCode {self.id} - {self.token[:8]}... - {'Available' if self.available else 'Unavailable'}"