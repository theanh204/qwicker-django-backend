from django.contrib.auth.models import AbstractUser
from django.db import models


class BaseModel(models.Model):
    updated_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class User(AbstractUser, BaseModel):
    role = models.ForeignKey('Role', related_name="user", on_delete=models.CASCADE, default=1)
    avatar = models.ImageField()

    def __str__(self):
        return self.get_full_name()


class Role(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Shipper(User):
    cmnd = models.CharField(max_length=12)


class Product(BaseModel):
    job = models.ForeignKey('Job', on_delete=models.CASCADE)
    description = models.CharField(max_length=255)
    type = models.ForeignKey('ProductType', on_delete=models.CASCADE)
    image = models.ImageField()
    length = models.IntegerField(null=False)
    width = models.IntegerField(null=False)
    height = models.IntegerField(null=False)
    weight = models.IntegerField(null=False)
    quantity = models.IntegerField(null=False)


class ProductType(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Job(BaseModel):
    type = models.ForeignKey('JobType', related_name='job_type', on_delete=models.CASCADE)
    description = models.CharField(max_length=255)
    shipment = models.ForeignKey('Shipment', related_name='job_shipment', on_delete=models.CASCADE)
    poster = models.ForeignKey(User, related_name='job_poster', on_delete=models.CASCADE)
    winner = models.ForeignKey(Shipper, related_name='job_winner', on_delete=models.CASCADE, null=True)


class JobType(models.Model):
    name = models.CharField(max_length=50)


class Auction(models.Model):
    job = models.ForeignKey(Job, related_name='auction_job', on_delete=models.CASCADE)
    shipper = models.ForeignKey(Shipper, related_name='auction_shipper', on_delete=models.CASCADE)
    time_joined = models.DateTimeField(auto_now=True)
    comment = models.CharField(max_length=255)
    start_date = models.DateTimeField()
    close_date = models.DateTimeField()
    # maybe add cost filed used for auctioning


class Shipment(models.Model):
    pick_up = models.ForeignKey('Address', related_name='shipment_pickup', on_delete=models.CASCADE)
    delivery_address = models.ForeignKey('Address', related_name='shipment_delivery_address', on_delete=models.CASCADE)
    ready_on = models.DateTimeField()
    collect_on = models.DateTimeField(null=True)
    delivered_on = models.DateTimeField(null=True)
    cost = models.DecimalField(max_digits=6, decimal_places=2)


class Address(models.Model):
    contact = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    country = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    street = models.CharField(max_length=50)
    home_number = models.CharField(max_length=10)
