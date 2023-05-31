from django.db import models
from django.contrib.auth.models import AbstractUser


class Electric(models.Model):
    ele_produc_id = models.AutoField
    product_name = models.CharField(max_length=50, default="")
    category = models.CharField(max_length=300, default="")
    desc = models.CharField(max_length=300, default="")
    price = models.IntegerField(default=0)
    pub_date = models.DateField()
    image = models.ImageField(upload_to="shop/images", default="image")

    def __str__(self):
        return self.product_name


class Contact(models.Model):
    msg_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=70, default="")
    phone = models.CharField(max_length=70, default="")
    desc = models.CharField(max_length=500, default="")

    def __str__(self):
        return self.name


class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    user_id = models.IntegerField(default=0)
    order_unique_id = models.CharField(max_length=100, default='')
    items_json = models.CharField(max_length=5000)
    name = models.CharField(max_length=90)
    email = models.CharField(max_length=111)
    address = models.CharField(max_length=111)
    city = models.CharField(max_length=111)
    state = models.CharField(max_length=111)
    phone = models.CharField(max_length=111, default="")
    zip_code = models.CharField(max_length=111)
    amount = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class OrderReport(models.Model):
    update_id = models.AutoField(primary_key=True)
    user_id = models.IntegerField(default=0)
    order_id = models.CharField(max_length=100, default='')
    update_desc = models.CharField(max_length=5000)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.update_desc[0:7] + "..."


class Cart(models.Model):
    cart_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=500, default='')
    qty = models.IntegerField(default=0)
    price = models.IntegerField(default=0)
    user_id = models.IntegerField(default=0)
    product_id = models.CharField(max_length=50, default="")

    def __str__(self):
        return self.name[0:17] + "..."


class Api(models.Model):
    api_id = models.IntegerField(default=0)
    name = models.CharField(max_length=50, default='')
    email = models.CharField(max_length=50, default='')
    street = models.CharField(max_length=50, default='')
    suite = models.CharField(max_length=50, default='')
    city = models.CharField(max_length=50, default='')
    zipcode = models.CharField(max_length=50,default=0)
    lat = models.CharField(max_length=50,default='')
    lng = models.CharField(max_length=50,default='')
    phone = models.CharField(max_length=50,default='')
    website = models.CharField(max_length=50, default='')
    company_name = models.CharField(max_length=100, default='')
    catchpharse = models.CharField(max_length=100, default='')
    bs = models.CharField(max_length=100, default='')

    def __str__(self):
        return self.name[0:17] + "..."
