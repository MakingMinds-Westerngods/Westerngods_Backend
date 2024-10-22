from django.shortcuts import render
from rest_framework import (generics, permissions, status)
from rest_framework.response import Response
from django.utils import timezone
from django.db.models import ProtectedError
from datetime import datetime
from PIL import Image
import base64
from django.core.files.images import ImageFile
import io
from django.db import IntegrityError, transaction
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
import firebase_admin
from firebase_admin import auth

import random


from .serializers import (ItemSerializer, ItemImagesSerializer,
                          OTPSerializer, WishlistSerializer, BagSerializer)
from .models import (Item, ItemImages, OTP, Wishlist, Bag)
from masters.models import Category
from masters.serializers import CategorySerializer


class ItemListView(generics.GenericAPIView):

    def post(self, request, format=None):
        with transaction.atomic():
            base = ((base64.b64decode(request.data['img']
                     [request.data['img'].find(",") + 1:])))
            image = Image.open(io.BytesIO(base))
            flname = 'item_image.jpeg'
            image_object = ImageFile(io.BytesIO(
                image.fp.getvalue()), name=flname)
            request.data.update({"image": image_object})
            serializer = ItemSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            for each in request.data['grnimagedata']:
                b = ((base64.b64decode(each['grnimage']
                     [each['grnimage'].find(",") + 1:])))
                img = Image.open(io.BytesIO(b))
                filename = 'item_images.jpeg'
                img_object = ImageFile(io.BytesIO(
                    img.fp.getvalue()), name=filename)
                each['item_image'] = img_object
                each.update({"item_id": serializer.data['id']})
                item_image_serializer = ItemImagesSerializer(data=each)
                item_image_serializer.is_valid(raise_exception=True)
                item_image_serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request, format=None):
        output = []
        if 'drop' in request.query_params:
            output = []
            queryset = Item.objects.all()
            serializer = ItemSerializer(queryset, many=True)
            for data in serializer.data:
                instance = {}
                instance.update({"label": data['name'], "value": data['id']})
                if instance not in output:
                    output.append(instance)
            return Response(output, status=status.HTTP_200_OK)
        queryset = Item.objects.all()
        serializer = ItemSerializer(queryset, many=True)
        for data in serializer.data:
            instance = {}
            category = Category.objects.filter(
                id_category=data['category']).get()
            instance.update({"category": category.name, "name": data['name'], "selling_price": data['selling_price'], "id": data['id'],
                             "count": data['count'], "rating": data['rating'], "cost_price": data['cost_price']})
            output.append(instance)
        return Response(output, status=status.HTTP_200_OK)


class ItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

    def get(self, request, pk, format=None):
        obj = self.get_object()
        serializer = self.get_serializer(obj)
        output = serializer.data
        id_category = Category.objects.filter(
            id_category=serializer.data['category']).get()
        output.update({"category": {"label": id_category.name,
                      "value": id_category.id_category}})
        item_images = ItemImages.objects.filter(item_id=serializer.data['id'])
        item_images_serializer = ItemImagesSerializer(
            item_images, many=True, context={"request": request})
        image_output = []
        for data in item_images_serializer.data:
            inst = {}
            inst.update(
                {"id": data['id_image'], "grnimage": data['item_image'], "item_id": data['item_id']})
            image_output.append(inst)
            print(image_output)
        output.update({"item_images": image_output})
        return Response(output, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        
        obj = self.get_object()
        with transaction.atomic():

            item_images_inDB = list(ItemImages.objects.filter(
                item_id=obj.id).values_list('id_image', flat=True))
            item_images_input = [each['id']
                                 for each in request.data['grnimagedata']]

            to_delete = []
            new_item = []

            for each in item_images_inDB:
                if each not in item_images_input:
                    to_delete.append(each)
            for each in item_images_input:
                if each not in item_images_inDB:
                    new_item.append(each)
            
            if 'data:image/' in request.data['image'][:30]:
                # update items  for which image is changed
                obj.image.delete()
                b = ((base64.b64decode( request.data['image'][ request.data['image'].find(",") + 1:])))
                img = Image.open(io.BytesIO(b))
                filename = 'item_image.jpeg'
                img_object = ImageFile(io.BytesIO(
                    img.fp.getvalue()), name=filename)
                request.data.update({"image": img_object})
                
                serializer = self.get_serializer(obj, data=request.data)
                serializer.is_valid(raise_exception=True)
                serializer.save()
            else:
                request.data.update({"image": obj.image})
                serializer = self.get_serializer(obj, data=request.data)
                serializer.is_valid(raise_exception=True)
                serializer.save()

            to_delete_items = ItemImages.objects.filter(id_image__in=to_delete)
            for each_item in to_delete_items:
                each_item.item_image.delete()
                each_item.delete()

            for each in request.data['grnimagedata']:
                if each['id'] in new_item:
                    # create  entries for new items included
                    each.update({"item_id": obj.id})
                    b = (
                        (base64.b64decode(each['grnimage'][each['grnimage'].find(",") + 1:])))
                    img = Image.open(io.BytesIO(b))
                    filename = 'item_img.jpeg'
                    img_object = ImageFile(io.BytesIO(
                        img.fp.getvalue()), name=filename)
                    each['item_image'] = img_object

                    item_image_serializer = ItemImagesSerializer(data=each)
                    item_image_serializer.is_valid(raise_exception=True)
                    item_image_serializer.save()
                else:
                    # update existing items
                    if 'data:image/' in each['grnimage'][:30]:
                        # update items  for which image is changed
                        b = (
                            (base64.b64decode(each['grnimage'][each['grnimage'].find(",") + 1:])))
                        img = Image.open(io.BytesIO(b))
                        filename = 'item_image.jpeg'
                        img_object = ImageFile(io.BytesIO(
                            img.fp.getvalue()), name=filename)
                        each['item_image'] = img_object

                        item_image = ItemImages.objects.get(id_image=each['id'])
                        item_image.item_image.delete()
                        item_image_serializer = ItemImagesSerializer(
                            item_image, data=each)
                        item_image_serializer.is_valid(raise_exception=True)
                        item_image_serializer.save()
                    else:
                        # update items  for which image is not changed
                        try:
                            item_image = ItemImages.objects.get(
                                id_image=each['id'])
                            item_image.item_id = item_image.item_id
                            item_image.item_image = item_image.item_image
                            item_image.save()
                        except IntegrityError:
                            return Response(
                                {
                                    "error_detail": ["Item image with this name already exists under this Item."]},
                                status=status.HTTP_400_BAD_REQUEST)
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    def delete(self, request, pk, format=None):
        obj = self.get_object()
        try:
            for each in ItemImages.objects.filter(item_id=obj):
                each.item_image.delete()
                each.delete()
            obj.delete()
        except ProtectedError:
            return Response({"error_detail": ["Item can't be deleted, as it is already in relation"]}, status=status.HTTP_423_LOCKED)
        return Response(status=status.HTTP_204_NO_CONTENT)


class UsersiteCategoryView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [AllowAny]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get(self, request, *args, **kwargs):
        queryset = Category.objects.all()
        serialiser = CategorySerializer(queryset, many=True)
        output = []
        for data in serialiser.data:
            category = {"id": data['id_category'], "category": data['name']}
            output.append(category)
        return Response(output, status=status.HTTP_200_OK)


class UsersiteItemListView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [AllowAny]
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

    def get(self, request, *args, **kwargs):
        queryset = Item.objects.filter(category=request.query_params['id'])
        serialiser = ItemSerializer(queryset, many=True)
        output = []
        for data in serialiser.data:
            item_data = ItemImages.objects.filter(item_id=data['id'])
            item_serialiser = ItemImagesSerializer(
                item_data, many=True, context={"request": request})
            inst = {}
            inst.update({"id": data['id'], "title": data['title'], "category": data['category'], "title": data['name'], "price": data['cost_price'], "rating": {
                        "rate": data['rating'], "count": data['count']}, "image": image_data[0], "image_data": []})
            for image in item_serialiser.data:
                image_data = {
                    "id": image['id_image'], "item_id": image['item_id'], "item_image": image['item_image']}
                inst["images"].append(image_data)
            output.append(inst)
        return Response(output, status=status.HTTP_200_OK)


# class GenerateOTPView(generics.GenericAPIView):
#     def post(self, request):
#         mobile_number = request.data['mobile_number']
#         print(mobile_number)
#         if not mobile_number:
#             return Response({'error': 'Mobile number is required'}, status=status.HTTP_400_BAD_REQUEST)

#         otp = str(random.randint(100000, 999999 ))

#         otp_record = OTP.objects.create(mobile_number=mobile_number, otp=otp)

#         # Send OTP via SMS
#         message = client.messages.create(
#             body=f'Your OTP is {otp}',
#             from_=TWILIO_PHONE_NUMBER,
#             to=mobile_number
#         )
#         print(otp)
#         print(otp_record)

#         serializer = OTPSerializer(otp_record)
#         return Response(serializer.data,status=status.HTTP_201_CREATED)

class VerifyOTPView(generics.GenericAPIView):
    def post(self, request):
        mobile_number = request.data.get('mobile_number')
        otp = request.data.get('otp')

        if not mobile_number or not otp:
            return Response({'error': 'Mobile number and OTP are required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            otp_record = OTP.objects.get(mobile_number=mobile_number, otp=otp)
            if otp_record.is_valid():
                return Response({'message': 'OTP is valid'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'OTP has expired'}, status=status.HTTP_400_BAD_REQUEST)
        except OTP.DoesNotExist:
            return Response({'error': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)


class SendOTPView(APIView):
    def post(self, request):
        mobile_number = request.data.get('mobile_number')
        if not mobile_number:
            return Response({'error': 'Mobile number is required'}, status=status.HTTP_400_BAD_REQUEST)

        # Format phone number with country code
        if not mobile_number.startswith('+'):
            return Response({'error': 'Mobile number must include the country code'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Send OTP via Firebase
            verification_id = auth.generate_phone_number_verification_code(
                mobile_number)
            return Response({'verification_id': verification_id}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class VerifyOTPView(APIView):
    def post(self, request):
        verification_id = request.data.get('verification_id')
        verification_code = request.data.get('verification_code')

        if not verification_id or not verification_code:
            return Response({'error': 'Verification ID and code are required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Verify OTP via Firebase
            auth.verify_phone_number(verification_id, verification_code)
            return Response({'message': 'OTP is valid'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class BagListView(generics.ListCreateAPIView):
    queryset = Bag.objects.all()
    serializer_class = BagSerializer

    def post(self, request, *args, **kwargs):
        request.data.update({"added_by":request.user.pk})
        obj = Wishlist.objects.filter(item_id=request.data['item_id']).get()
        if obj.item_id == request.data['item_id']:
            obj.delete()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get(self, request):
        bag = Bag.objects.all()
        serializer = self.get_serializer(bag, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class BagDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Bag.objects.all()
    serializer_class = BagSerializer

    def get(self, request, *args, **kwargs):
        bag = self.get_object()
        serializer = self.get_serializer(bag)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        bag = self.get_object()
        serializer = self.get_serializer(bag, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({serializer.data})

    def delete(self, request, *args, **kwargs):
        bag = self.get_object()
        bag.delete()
        return Response({'message': 'Bag deleted'}, status=status.HTTP_200_OK)
