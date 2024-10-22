from rest_framework import serializers
from .models import (Item,ItemImages,OTP,Wishlist,Bag)
from rest_framework.validators import UniqueTogetherValidator


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'
        
        
class ItemImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemImages
        fields = '__all__'
        
class OTPSerializer(serializers.ModelSerializer):
    class Meta:
        model = OTP
        fields = '__all__'


class WishlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wishlist
        fields = '__all__'
        validators = [
            UniqueTogetherValidator(
                queryset=Wishlist.objects.all(),
                fields=(
                    'added_by',
                    'item_id',),
                message='This item has been already added in your wishlist')]
class BagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bag
        fields = '__all__'
        
        
