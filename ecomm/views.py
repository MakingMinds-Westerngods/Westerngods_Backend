from datetime import datetime, timedelta
from random import randint
from django.conf import settings
from django.forms import model_to_dict
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from knox.models import AuthToken
from rest_framework import generics, status
from django.db import IntegrityError
from django.utils import timezone
from django.db.models import Q, ProtectedError
from models_logging.models import Change
from django.utils.timezone import utc
from django.http import Http404
from django.core.mail import send_mail
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError
from cryptography.fernet import Fernet, InvalidToken
from django.template.loader import render_to_string
import dotenv
import os
from django.contrib.auth.hashers import make_password


# local imports
from custom.permissions import isAdmin, isSuperuser
from masters.models import (Category)
from masters.serializers import (CategorySerializer)
from inventory.models import (Item, ItemImages, Wishlist)
from inventory.serializers import (ItemSerializer, ItemImagesSerializer, WishlistSerializer)
from masters.models import (Category)
from masters.serializers import (CategorySerializer)
from .constants import (productdatafront, tshirtdata, hoodiedata, menuList)


class ProductListView(generics.GenericAPIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        output = productdatafront
        return Response(output, status=status.HTTP_200_OK)


class TshirtListView(generics.GenericAPIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        output = tshirtdata
        return Response(output, status=status.HTTP_200_OK)


class HoodieListView(generics.GenericAPIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        output = hoodiedata
        return Response(output, status=status.HTTP_200_OK)
    
class WishlistListView(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    queryset = Wishlist.objects.all()
    serializer_class = WishlistSerializer

    def post(self, request, *args, **kwargs):
        request.data.update({"added_by":request.user.pk})
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get(self, request):
        output = []
        wishlist = Wishlist.objects.filter(added_by=request.user)
        serializer = self.get_serializer(wishlist, many=True)
        for data in serializer.data:
            product = Item.objects.get(id=data['item_id'])
            product_serializer = ItemSerializer(product, context={"request":request})
            data.update({"product":product_serializer.data})
            if data not in output:
                output.append(data)
        return Response(output, status=status.HTTP_200_OK)
    
class wishlistDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [AllowAny]
    queryset = Wishlist.objects.all()
    serializer_class = WishlistSerializer

    def get(self, request, *args, **kwargs):
        wishlist = self.get_object()
        serializer = self.get_serializer(wishlist)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        wishlist = self.get_object()
        wishlist.delete()
        return Response({'message': 'Item has been deleted from your wishlist.'}, status=status.HTTP_200_OK)


class CategoryListView(generics.GenericAPIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        output = []
        categories = Category.objects.all()
        categories_serializer = CategorySerializer(categories, many=True)
        for data in categories_serializer.data:
            try:
                category_images = []
                items = Item.objects.filter(
                    category=data['id_category']).order_by('-pk')[:4]
                item_serializer = ItemSerializer(items, many=True)
                for item in item_serializer.data:
                    category_images.append({"img": item['image']})
                data.update({"cat_images": category_images})
                if data not in output:
                    output.append(data)
            except Exception:
                pass
        return Response(output, status=status.HTTP_200_OK)


class CategoryProductsList(generics.GenericAPIView):
    permission_classes = [AllowAny]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get(self, request, *args, **kwargs):
        print(request.user.pk)
        output = []
        obj = self.get_object()
        item_query = Item.objects.filter(category=obj.id_category)
        item_serializer = ItemSerializer(
            item_query, many=True, context={"request": request})
        for data in item_serializer.data:
            data.update({"title": data["name"]})
            if(Wishlist.objects.filter(added_by=request.user.pk, item_id=data['id']).exists()):
                wishlist_obj = Wishlist.objects.filter(added_by=request.user.pk, item_id=data['id']).get()
                data.update({"is_in_wishlist":True, "wishlist_id":wishlist_obj.id})
            else:
                data.update({"is_in_wishlist":False})
            if data not in output:
                output.append(data)
        return Response(output, status=status.HTTP_200_OK)


class ItemDetailsView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

    def get(self, request, *args, **kwargs):
        obj = self.get_object()
        item_serializer = ItemSerializer(obj, context={"request": request})
        instance = {}
        item_image_query = ItemImages.objects.filter(item_id=obj.id)
        item_image_serializer = ItemImagesSerializer(
            item_image_query, many=True, context={"request": request})
        instance.update({"id": obj.id, "name": obj.name, "title": obj.name, "image": item_serializer.data['image'], "description": obj.description,
                         "rating": obj.rating, "price": obj.cost_price, "cost_price": obj.cost_price, "description": obj.description,
                         "product_description":obj.product_description,"box_description":obj.box_description})
        instance.update({"item_images": item_image_serializer.data})
        return Response(instance, status=status.HTTP_200_OK)


class NavMenuList(generics.GenericAPIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        output = [
                {
                "menu": "Shop",
                "submenu": []
                },
                {
                "menu": "About",
                },
                ]
        parent_category_query = ParentCategory.objects.filter(is_active=True)
        parent_category_serializer = ParentCategorySerializer(
            parent_category_query, many=True)
        for data in parent_category_serializer.data:
            instance = {}
            category_query = Category.objects.filter(
                parent_category=data['id'])
            category_serializer = CategorySerializer(category_query, many=True)
            instance.update({"categoty": data['name']})
            items = []
            for categories in category_serializer.data:
                cat_instance = {}
                cat_instance.update(
                    {"id": categories['id_category'], "name": categories['name'], "path": "/products/"+categories['name']+"&"+str(categories['id_category'])})
                if cat_instance not in items:
                    items.append(cat_instance)
            instance.update({"items": items})
        if instance not in output[0]['submenu']:
            output[0]['submenu'].append(instance)
        return Response(output, status=status.HTTP_200_OK)


class ItemAllImagesView(generics.ListAPIView):
    permission_classes = [AllowAny]
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

    def get(self, request, *args, **kwargs):
        output = []
        if 'asc' in request.query_params:
            queryset=Item.objects.all().order_by("cost_price")
        elif "desc" in request.query_params:
            queryset=Item.objects.all().order_by("-cost_price")
        else:
            queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        for data in serializer.data:
            instance = {}
            category = Category.objects.filter(
                id_category=data["category"]).get()
            image_queryset = ItemImages.objects.filter(item_id=data["id"])
            image_seri = ItemImagesSerializer(
                image_queryset, many=True, context={"request": request})
            if(Wishlist.objects.filter(added_by=request.user.pk, item_id=data['id']).exists()):
                wishlist_obj = Wishlist.objects.filter(added_by=request.user.pk, item_id=data['id']).get()
                instance.update({"is_in_wishlist":True, "wishlist_id":wishlist_obj.id})
            else:
                instance.update({"is_in_wishlist":False})

        
            

            image_output = []  # Reset image_output for each item
            for image_data in image_seri.data:
                image_inst = {
                    "id": image_data["id_image"],
                    "item_image": image_data["item_image"]
                }
                image_output.append(image_inst)

            # Check if image_seri.data has any images
            if image_seri.data:
                # Get the first image from image_seri.data
                first_image_data = image_seri.data[0]
                image_instance = {
                    "id": first_image_data["id_image"],
                    "item_image": first_image_data["item_image"]
                }
            else:
                image_instance = {
                    "id": None,
                    "item_image": None
                }
            # size_instance={"xs": data["xs"], "sm": data["sm"], "md": data["md"],
            #                      "lg": data["lg"], "xl": data["xl"], "xxl": data["xxl"]}
           
            

            instance.update({
                "id": data["id"],
                "title": data["name"],
                "name": data["name"],
                "brand": data["name"],
                "selling_price": data["selling_price"],
                "cost_price": data["cost_price"],
                "description": data["description"],
                # "size": size_instance,
                "product_description": data["product_description"],
                "category": category.name,
                "image": image_instance["item_image"],
                "image_data": image_output,  # Include only the images for this item
                "rating": {
                    "rate": data["cost_price"],
                    "count": data["count"]
                }
            })

            output.append(instance)

        return Response(output, status=status.HTTP_200_OK)
    
class ItemImagesHomeView(generics.ListAPIView):
    permission_classes = [AllowAny]
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

    def get(self, request, *args, **kwargs):
        output = []

        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        for data in serializer.data:
            instance = {}
            category = Category.objects.filter(
                id_category=data["category"]).get()
            image_queryset = ItemImages.objects.filter(item_id=data["id"])
            image_seri = ItemImagesSerializer(
                image_queryset, many=True, context={"request": request})
            if(Wishlist.objects.filter(added_by=request.user.pk, item_id=data['id']).exists()):
                wishlist_obj = Wishlist.objects.filter(added_by=request.user.pk, item_id=data['id']).get()
                instance.update({"is_in_wishlist":True, "wishlist_id":wishlist_obj.id})
            else:
                instance.update({"is_in_wishlist":False})

        
            

            image_output = []  # Reset image_output for each item
            for image_data in image_seri.data:
                image_inst = {
                    "id": image_data["id_image"],
                    "item_image": image_data["item_image"]
                }
                image_output.append(image_inst)

            # Check if image_seri.data has any images
            if image_seri.data:
                # Get the first image from image_seri.data
                first_image_data = image_seri.data[0]
                image_instance = {
                    "id": first_image_data["id_image"],
                    "item_image": first_image_data["item_image"]
                }
            else:
                image_instance = {
                    "id": None,
                    "item_image": None
                }
            # size_instance={"xs": data["xs"], "sm": data["sm"], "md": data["md"],
            #                      "lg": data["lg"], "xl": data["xl"], "xxl": data["xxl"]}
           
            

            instance.update({
                "id": data["id"],
                "title": data["name"],
                "name": data["name"],
                "brand": data["name"],
                "selling_price": data["selling_price"],
                "cost_price": data["cost_price"],
                "description": data["description"],
                "product_description": data["product_description"],
                # "size": size_instance,
                "category": category.name,
                "image": image_instance["item_image"],
                "image_data": image_output,  # Include only the images for this item
                "rating": {
                    "rate": data["cost_price"],
                    "count": data["count"]
                }
            })

            output.append(instance)

        return Response(output[:4], status=status.HTTP_200_OK)


class SearchItemsView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    
    def post(self, request, *args, **kwargs):
        instance = {}
        category_output = []
        categories = Category.objects.filter(name__icontains = request.data['search'])
        categories_serializer = CategorySerializer(categories, many=True)
        for data in categories_serializer.data:
            items = Item.objects.filter(category=data['id_category']).earliest('id')
            items_seri = ItemSerializer(items, context = {"request":request})
            data.update({"image":items_seri.data['image']})
            data.update({"path": "/products/"+data['name']+"&"+str(data['id_category'])})
            
            if data not in category_output:
                category_output.append(data)
        products = Item.objects.filter(name__icontains = request.data['search'])
        products_serializer = ItemSerializer(products, many=True, context = {"request":request})
        instance.update({"products":products_serializer.data, "collections":category_output})
        return Response(instance, status=status.HTTP_200_OK)