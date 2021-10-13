from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits = 9, decimal_places=0)
    image = CloudinaryField('image')
    city = models.CharField(max_length=100, default='')

    def __str__(self):
        return f"{self.user}"

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=9, decimal_places=0, default=0)

    def __str__(self):
        return f"{self.user}'s Cart"

class Item(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey('api.Product', on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField()
    subtotal = models.DecimalField(max_digits=9, decimal_places=0, default=0)

    def __str__(self):
        return f"{self.cart} | {self.product}"
