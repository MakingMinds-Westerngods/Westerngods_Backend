from django.db import models
from django.utils import timezone
from datetime import datetime
import random
import os


def upload_to_gal_item(instance, filename):
    _, file_extension = os.path.splitext(filename)
    return 'images/item/item_images/{title}_{ext}'.format(title=instance.item_id, ext=file_extension)


def upload_to_gal(instance, filename):
    _, file_extension = os.path.splitext(filename)
    return 'images/item/item_image/{title}_{ext}'.format(title=instance.name, ext=file_extension)


# Item
class Item(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=200)
    category = models.ForeignKey("masters.Category", on_delete=models.PROTECT)
    item_type = models.CharField(max_length=20,  choices=(
        ("1", "Goods"), ("2", "Service"),), default=1)
    sku = models.CharField(max_length=30, null=True, blank=True)
    returnable_item = models.BooleanField(default=True)
    dimensions = models.CharField(max_length=30, null=True, blank=True)
    dimension_type = models.CharField(
        max_length=20,  choices=(("1", "cm"), ("2", "in"),), default=1)
    weight = models.CharField(max_length=30, null=True, blank=True)
    weight_type = models.CharField(max_length=20,  choices=(
        ("1", "kg"), ("2", "g"), ("2", "lb"), ("2", "oz"),), default=1)
    mpn = models.CharField(max_length=30, null=True, blank=True)
    upc = models.CharField(max_length=30, null=True, blank=True)
    isbn = models.CharField(max_length=30, null=True, blank=True)
    ean = models.CharField(max_length=30, null=True, blank=True)
    count = models.CharField(max_length=100, null=True, blank=True)
    selling_price = models.CharField(max_length=30, null=True, blank=True)
    cost_price = models.CharField(max_length=30, null=True, blank=True)
    account = models.CharField(max_length=30, null=True, blank=True)
    rating = models.CharField(max_length=30)
    description = models.CharField(max_length=70, null=True, blank=True)
    opening_stock = models.CharField(max_length=30, null=True, blank=True)
    opening_stock_per_unit = models.CharField(
        max_length=30, null=True, blank=True)
    reorder_point = models.CharField(max_length=30, null=True, blank=True)
    image = models.ImageField(upload_to=upload_to_gal, blank=True, null=True)
    product_description=models.TextField(max_length=1000)
    box_description=models.TextField(max_length=1000)

    class Meta:
        db_table = 'item'


class ItemImages(models.Model):
    id_image = models.BigAutoField(primary_key=True)
    item_id = models.ForeignKey(
        Item, on_delete=models.CASCADE, related_name='item_id_images')
    item_image = models.ImageField(
        upload_to=upload_to_gal_item, blank=True, null=True)

    class Meta:
        # managed=True
        db_table = 'item_images'


class OTP(models.Model):
    mobile_number = models.CharField(max_length=15)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_valid(self):
        return timezone.now() < self.created_at + timezone.timedelta(minutes=5)

    class Meta:
        db_table = 'otp'


class Wishlist(models.Model):
    id = models.BigAutoField(primary_key=True)
    item_id = models.ForeignKey('inventory.Item', on_delete=models.PROTECT)
    added_on = models.DateTimeField(auto_now_add=datetime.now())
    added_by = models.ForeignKey(
        'accounts.user', on_delete=models.PROTECT, related_name="wishlist_added_by")

    class Meta:
        db_table = 'wishlist'


class Bag(models.Model):
    id = models.BigAutoField(primary_key=True)
    item_id = models.ForeignKey(Item, on_delete=models.PROTECT)
    added_on = models.DateTimeField(auto_now_add=datetime.now())
    added_by = models.ForeignKey(
        'accounts.user', on_delete=models.PROTECT, related_name="bag_added_by")
    size=models.CharField(max_length=10)
    quantity = models.CharField(max_length=20, null=True)

    class Meta:
        db_table = 'bag'
