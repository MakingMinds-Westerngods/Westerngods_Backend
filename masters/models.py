from django.db import models
from datetime import datetime, timedelta, date
import os

def upload_to_gal(instance, filename):
    _, file_extension = os.path.splitext(filename)
    return 'images/banner/banner_image/{title}_{ext}'.format(title=instance.banner_name, ext=file_extension)

def upload_to_grid(instance, filename):
    _, file_extension = os.path.splitext(filename)
    return 'images/grid/grid_image/{title}_{ext}'.format(title=instance.grid_item_name, ext=file_extension)


class Country(models.Model):
    id = models.AutoField(primary_key=True)
    shortname = models.CharField(max_length=3, unique=True)
    name = models.CharField(max_length=150)
    currency_name = models.CharField(max_length=10)
    currency_code = models.CharField(max_length=4)
    mob_code = models.CharField(max_length=5)
    mob_no_len = models.PositiveIntegerField()
    created_on = models.DateTimeField(auto_now_add=datetime.now())
    created_by = models.ForeignKey(
        'accounts.User', related_name='country_by_user', on_delete=models.PROTECT)
    updated_on = models.DateTimeField( null=True)
    updated_by = models.ForeignKey(
        'accounts.User', related_name='country_updated_by_user', null=True, on_delete=models.SET_NULL)

    class Meta:
        db_table = 'country'

    LOGGING_IGNORE_FIELDS = ('created_on', 'created_by', 'updated_on',
                             'updated_by')


class State(models.Model):
    id = models.AutoField(primary_key=True)
    state_name = models.CharField(max_length=50, unique=True)
    country = models.ForeignKey('Country', on_delete=models.PROTECT)
    created_on = models.DateTimeField(auto_now_add=datetime.now())
    created_by = models.ForeignKey(
        'accounts.User', related_name='state_by_user', on_delete=models.PROTECT)
    updated_on = models.DateTimeField(null=True)
    updated_by = models.ForeignKey(
        'accounts.User', related_name='state_updated_by_user', null=True, on_delete=models.SET_NULL)

    def __str__(self) -> str:
        return 'State - ' + str(self.pk)

    class Meta:
        db_table = 'state'

    LOGGING_IGNORE_FIELDS = ('created_on', 'created_by', 'updated_on',
                             'updated_by')

    
class District(models.Model):
    id=models.AutoField(primary_key=True)
    district_name=models.CharField(max_length=50, unique=True)
    state=models.ForeignKey('State',on_delete=models.PROTECT)
    district_code=models.CharField(max_length=10,unique=True)
    created_by = models.ForeignKey(
        'accounts.User', related_name='district_by_user', on_delete=models.PROTECT)
    created_on = models.DateTimeField(auto_now_add=True, null=True)
    updated_on = models.DateTimeField(null=True)
    updated_by = models.ForeignKey(
        'accounts.User', related_name='district_updated_by_user', null=True, on_delete=models.SET_NULL)
    
    class Meta:
        db_table = 'district'
    
    LOGGING_IGNORE_FIELDS = ('created_on', 'created_by', 'updated_on',
                             'updated_by')
        
        
class City(models.Model):
    id = models.AutoField(primary_key=True)
    state = models.ForeignKey('State', on_delete=models.PROTECT)
    district=models.ForeignKey('District',on_delete=models.PROTECT)
    city_name = models.CharField(max_length=70)
    created_on = models.DateTimeField(auto_now_add=datetime.now())
    created_by = models.ForeignKey(
        'accounts.User', related_name='city_by_user', on_delete=models.PROTECT)
    updated_on = models.DateTimeField(null=True)
    updated_by = models.ForeignKey(
        'accounts.User', related_name='city_updated_by_user', null=True, on_delete=models.SET_NULL)

    def __str__(self) -> str:
        return 'City - ' + str(self.pk)

    class Meta:
        db_table = 'city'

    LOGGING_IGNORE_FIELDS = ('created_on', 'created_by', 'updated_on',
                             'updated_by')
    

# class ParentCategory(models.Model):
#     id=models.BigAutoField(primary_key=True)
#     name=models.CharField(max_length=30)
#     short_code=models.CharField(max_length=30)
#     description=models.TextField(max_length=100, null=True)
#     is_active = models.BooleanField(default=True)
    
#     class Meta:
#         db_table = "parent_category"

class Category(models.Model):
    id_category=models.BigAutoField(primary_key=True)
    name=models.CharField(max_length=30)
    short_code=models.CharField(max_length=30)
    short_description=models.TextField(max_length=100)
    long_description=models.TextField(max_length=100)
    keyword=models.CharField(max_length=15)
    is_active = models.BooleanField(default=1)
    
    class Meta:
        db_table = "category"


class Unit(models.Model):
    id=models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=200)
    unit_code=models.CharField(max_length=15)
    description= models.CharField(max_length=200, null=True)
    class Meta:
        db_table = 'unit'
        
class Manufacturer(models.Model):
    id=models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=200)
    manufacturer_code=models.CharField(max_length=15)
    description= models.CharField(max_length=200, null=True)
    class Meta:
        db_table = 'manufracturer'
        
        
class Brand(models.Model):
    id=models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=200)
    brand_code=models.CharField(max_length=15)
    description= models.CharField(max_length=200, null=True)
    class Meta:
        db_table = 'brand'
        
        
class SalesAccount(models.Model):
    id=models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=200)
    sales_account_code=models.CharField(max_length=15)
    description= models.CharField(max_length=200, null=True)
    class Meta:
        db_table = 'sales_account'
        
class PurchaseAccount(models.Model):
    id=models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=200)
    purchase_account_code=models.CharField(max_length=15)
    description= models.CharField(max_length=200, null=True)
    class Meta:
        db_table = 'purchase_account'

class Banner(models.Model):
    banner_id=models.BigAutoField(primary_key=True)
    banner_name=models.CharField(max_length=30)
    banner_status=models.BooleanField(default=True)
    banner_description=models.CharField(max_length=100)
    banner_img=models.ImageField(upload_to=upload_to_gal, blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=datetime.now())
    created_by = models.ForeignKey(
        'accounts.User', related_name='banner_by_user', on_delete=models.PROTECT)
    updated_on = models.DateTimeField(null=True)
    updated_by = models.ForeignKey(
        'accounts.User', related_name='banner_updated_by_user', null=True, on_delete=models.SET_NULL)

    class Meta:
        db_table = 'banner'

class OfferSlide(models.Model):
    offer_slider_id=models.BigAutoField(primary_key=True)
    offer_slider_content=models.TextField(max_length=100,null=True)
    offer_slider_status=models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=datetime.now())
    created_by = models.ForeignKey(
        'accounts.User', related_name='offerslide_by_user', on_delete=models.PROTECT)
    updated_on = models.DateTimeField(null=True)
    updated_by = models.ForeignKey(
        'accounts.User', related_name='offerslide_updated_by_user', null=True, on_delete=models.SET_NULL)

    class Meta:
        db_table = 'offerslide'
        

class GridItem(models.Model):
    grid_item_id=models.BigAutoField(primary_key=True)
    grid_item_name=models.CharField(max_length=30)
    image=models.ImageField(upload_to=upload_to_grid, blank=True, null=True)
    grid_content =models.TextField()
    grid_title =models.CharField(max_length=50)
    status=models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=datetime.now())
    created_by = models.ForeignKey(
        'accounts.User', related_name='grid_by_user', on_delete=models.PROTECT)
    updated_on = models.DateTimeField(null=True)
    updated_by = models.ForeignKey(
        'accounts.User', related_name='grid_updated_by_user', null=True, on_delete=models.SET_NULL)

    class Meta:
        db_table = 'griditem'
        
    
