from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

# Create your models here.
class Product(models.Model):
    seller = models.ForeignKey('account.Profile', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products')
    name = models.CharField(max_length=100)
    desc = models.TextField()
    price = models.DecimalField(max_digits = 9, decimal_places=0)
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=0)
    stock = models.PositiveIntegerField(default=1)
    sold = models.PositiveIntegerField(default=0)
    date_added = models.DateTimeField(default=now)

    def __str__(self):
        return self.name

class Review(models.Model):
    rate = (
        (1, 'Very Bad'),
        (2, 'Bad'),
        (3, 'Mediocre'),
        (4, 'Good'),
        (5, 'Very Good')
        )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    reviewer = models.ForeignKey('account.Profile', on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(choices=rate)
    review = models.CharField(max_length=500, default='')

    def __str__(self):
        return str(self.product) + " | " + str(self.rating)

class BoughtItem(models.Model):
    stat = (
        (1, 'Processed By Seller'),
        (2, 'In Shipping'),
        (3, 'Made It')
    )
    buyer = models.ForeignKey('account.Profile', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=1)
    status = models.PositiveSmallIntegerField(choices=stat, default=1)
    date_bought = models.DateTimeField(default=now)

    def __str__(self):
        return f"{self.product} | {self.buyer}"
