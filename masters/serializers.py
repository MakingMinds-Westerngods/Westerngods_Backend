from rest_framework import serializers

from .models import (Category, Brand, SalesAccount,Banner, PurchaseAccount, Manufacturer, Unit, Country, State,OfferSlide,GridItem,
                     City, District)

class CountrySerializer(serializers.ModelSerializer):

    class Meta:
        model = Country
        fields = '__all__'
        
#District
class DistrictSerializer(serializers.ModelSerializer):

    class Meta:
        model = District
        fields = '__all__'


# State model serializer
class StateSerializer(serializers.ModelSerializer):

    class Meta:
        model = State
        fields = '__all__'


# City model serializer
class CitySerializer(serializers.ModelSerializer):

    class Meta:
        model = City
        fields = '__all__'
        
        
class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'
        
        
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
        
        
class SalesAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesAccount
        fields = '__all__'
        
        
        
class PurchaseAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseAccount
        fields = '__all__'
        
        
class ManufacturerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manufacturer
        fields = '__all__'
        
        
class UnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unit
        fields = '__all__'
        
class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = '__all__'
        
class OfferSlideSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfferSlide
        fields = '__all__'


class GridItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = GridItem
        fields = '__all__'
        
        

        
