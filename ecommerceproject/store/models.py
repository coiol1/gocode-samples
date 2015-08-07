from django.db import models

# Create your models here.
class Order(models.Model):
    status = models.IntegerField()
    status_legend = {1: 'in cart', 2: 'ordered'}
    username = models.CharField(max_length = 128)

    def get_status(self):
        return self.status_legend[self.status]

class Product(models.Model):
    name = models.CharField(max_length = 128)
    price = models.IntegerField()
    image = models.TextField()
    description = models.TextField()
    orderproducts = models.ManyToManyField(Order, through = "OrderProduct")

    def dollars(self):
        if self.price <= 99999:
            return "%.2f" % (self.price / 100.0)
        else:
            return '{:,.2f}'.format(self.price / 100.0)

class OrderProduct(models.Model):
    order = models.ForeignKey(Order)
    product = models.ForeignKey(Product)
    quantity = models.IntegerField()