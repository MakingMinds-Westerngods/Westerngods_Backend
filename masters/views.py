from django.shortcuts import render
from rest_framework import (generics, permissions, status)
from rest_framework.response import Response
from django.utils import timezone
from django.db.models import ProtectedError
from datetime import datetime
from custom.permissions import isAdmin
from django.db import IntegrityError
from rest_framework.permissions import AllowAny

from .serializers import (BrandSerializer, UnitSerializer, SalesAccountSerializer,OfferSlideSerializer,GridItemSerializer,BannerSerializer,                       
                          PurchaseAccountSerializer, ManufacturerSerializer, CategorySerializer, CountrySerializer,
                          StateSerializer, CitySerializer, DistrictSerializer)
from .models import (Manufacturer, Brand, Unit, SalesAccount, PurchaseAccount,Banner,OfferSlide,GridItem,
                     Category, Country, State, District, City)


class CountryView(generics.GenericAPIView):
    permission_classes = [isAdmin]

    def get(self, request, *args, **kwargs):
        if 'countrydrop' in request.query_params:
            output = []
            queryset = Country.objects.all()
            serializer = CountrySerializer(queryset, many=True)
            for data in serializer.data:
                instance = {}
                instance.update(
                    {"label": data['name'], "value": data['id']})
                if instance not in output:
                    output.append(instance)
            return Response(output, status=status.HTTP_200_OK)
        queryset = Country.objects.all()
        serializer = CountrySerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        request.data.update({"created_by": request.user.pk})
        serializer = CountrySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CountryDetailsView(generics.GenericAPIView):
    permission_classes = [isAdmin]
    queryset = Country.objects.all()
    serializer_class = CountrySerializer

    def get(self, request, *args, **kwargs):
        country = self.get_object()
        serializer = self.get_serializer(country)
        output = serializer.data
        output.update({"created_by": country.created_by.username,
                       "updated_by": country.updated_by.username if country.updated_by != None else None})
        return Response(output, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        country = self.get_object()
        request.data.update({"updated_by": request.user.pk,
                            "updated_on": datetime.now(tz=timezone.utc), "created_by": country.created_by.pk})
        serializer = self.get_serializer(country, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class StateView(generics.GenericAPIView):
    permission_classes = [isAdmin]
    queryset = State.objects.all()
    serializer_class = StateSerializer

    def post(self, request, *args, **kwargs):
        request.data.update({"created_by": request.user.pk})
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request, *args, **kwargs):
        if 'country' in request.query_params:
            queryset = State.objects.filter(
                country=request.query_params['country'])
            serializer = StateSerializer(queryset, many=True)
            output = []
            for data in serializer.data:
                instance = {}
                instance.update(
                    {"value": data['id'], "label": data['state_name']}
                )
                if instance not in output:
                    output.append(instance)
            return Response(output)
        if 'options' in request.query_params:
            queryset = self.get_queryset()
            serializer = self.get_serializer(queryset, many=True)
            output = []
            for data in serializer.data:
                instance = {}
                instance.update(
                    {"value": data['id'], "label": data['state_name']}
                )
                if instance not in output:
                    output.append(instance)
            return Response(output, status=status.HTTP_200_OK)
        return Response(State.objects.all().values(), status=status.HTTP_200_OK)


class StateDetailsView(generics.GenericAPIView):
    permission_classes = [isAdmin]
    queryset = State.objects.all()
    serializer_class = StateSerializer

    def get(self, request, *args, **kwargs):
        state = self.get_object()
        serializer = self.get_serializer(state)
        output = serializer.data
        output.update({"country": {"label": state.country.name,
                      "value": state.country.id, }})
        output.update({"created_by": state.created_by.username,
                       "updated_by": state.updated_by.username if state.updated_by != None else None})
        return Response(output, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        state = self.get_object()
        request.data.update({"updated_by": request.user.pk,
                            "updated_on": datetime.now(tz=timezone.utc), "created_by": state.created_by.pk})
        serializer = self.get_serializer(state, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)


class DistrictView(generics.GenericAPIView):
    permission_classes = [isAdmin]
    serializer_class = DistrictSerializer
    queryset = District.objects.all()

    def post(self, request, *args, **kwargs):
        request.data.update({"created_by": request.user.pk})
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request, *args, **kwargs):
        if 'state' in request.query_params:
            queryset = District.objects.filter(
                state=request.query_params['state'])
            serializer = DistrictSerializer(queryset, many=True)
            output = []
            for data in serializer.data:
                instance = {}
                instance.update(
                    {"value": data['id'],
                     "label": data['district_name']}
                )
                if instance not in output:
                    output.append(instance)
            return Response(output, status=status.HTTP_200_OK)
        vari = self.get_serializer(City.objects.all(), many=True)
        output2 = []
        for data2 in vari.data:
            instance2 = {}
            state = State.objects.filter(id=data2['state']).get()
            instance2.update(
                {"label": data2['id'], "value": data2['district_name'], "state_name": state.state_name})
            if instance2 not in output2:
                output2.append(instance2)
        return Response(output2, status=status.HTTP_200_OK)


class DistrictDetailsView(generics.RetrieveDestroyAPIView):
    permission_classes = [isAdmin]
    serializer_class = DistrictSerializer
    queryset = District.objects.all()

    def get(self, request, *args, **kwargs):
        district = self.get_object()
        serializer = self.get_serializer(district)
        output = serializer.data
        output.update({"state": {"label": district.state.state_name,
                      "value": district.state.id, }})
        output.update({"created_by": district.created_by.username,
                       "updated_by": district.updated_by.username if district.updated_by != None else None})
        return Response(output, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        city = self.get_object()
        request.data.update({"updated_by": request.user.pk,
                            "updated_on": datetime.now(tz=timezone.utc), "created_by": city.created_by.pk})
        serializer = self.get_serializer(city, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    def delete(self, request, *args, **kwargs):
        city = self.get_object()
        city.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CityView(generics.GenericAPIView):
    permission_classes = [isAdmin]
    serializer_class = CitySerializer
    queryset = City.objects.all()

    def post(self, request, *args, **kwargs):
        request.data.update({"created_by": request.user.pk})
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request, *args, **kwargs):
        if 'state' in request.query_params:
            queryset = City.objects.all().filter(
                state=request.query_params['code'])
            serializer = CitySerializer(queryset, many=True)
            output = []
            for data in serializer.data:
                instance = {}
                instance.update(
                    {"value": data['id'],
                     "label": data['city_name']}
                )
                if instance not in output:
                    output.append(instance)
            return Response(output, status=status.HTTP_200_OK)
        vari = self.get_serializer(City.objects.all(), many=True)
        output2 = []
        for data2 in vari.data:
            instance2 = {}
            state2 = State.objects.filter(id=data2['state']).get()
            district = District.objects.filter(id=data2['district']).get()
            instance2.update(
                {"label": data2['id'], "value": data2['city_name'], "state_name": state2.state_name,
                 "district_name": district.district_name})
            if instance2 not in output2:
                output2.append(instance2)
        return Response(output2, status=status.HTTP_200_OK)


class CityDetailsView(generics.RetrieveDestroyAPIView):
    permission_classes = [isAdmin]
    serializer_class = CitySerializer
    queryset = City.objects.all()

    def get(self, request, *args, **kwargs):
        city = self.get_object()
        serializer = self.get_serializer(city)
        output = serializer.data
        output.update({"state": {"label": city.state.state_name,
                      "value": city.state.id, }})
        output.update({"district": {"label": city.district.district_name,
                      "value": city.district.id, }})
        output.update({"created_by": city.created_by.username,
                       "updated_by": city.updated_by.username if city.updated_by != None else None})
        return Response(output, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        city = self.get_object()
        request.data.update({"updated_by": request.user.pk,
                            "updated_on": datetime.now(tz=timezone.utc), "created_by": city.created_by.pk})
        serializer = self.get_serializer(city, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    def delete(self, request, *args, **kwargs):
        city = self.get_object()
        city.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# class ParentCategoryListView(generics.GenericAPIView):
#     permission_classes = [isAdmin]
#     queryset = ParentCategory.objects.all()
#     serializer_class = ParentCategorySerializer

#     def post(self, request, *args, **kwargs):
#         serializer = ParentCategorySerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)

#     def get(self, request, *args, **kwargs):
#         if 'drop' in request.query_params:
#             output = []
#             queryset = ParentCategory.objects.filter(is_active=True)
#             serializer = ParentCategorySerializer(queryset, many=True)
#             for data in serializer.data:
#                 instance = {}
#                 instance.update({"label": data['name'], "value": data['id']})
#                 if instance not in output:
#                     output.append(instance)
#             return Response(output, status=status.HTTP_200_OK)
#         queryset = ParentCategory.objects.all()
#         serializer = ParentCategorySerializer(queryset, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)


# class ParentCategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
#     permission_classes = [isAdmin]
#     queryset = ParentCategory.objects.all()
#     serializer_class = ParentCategorySerializer

#     def get(self, request, *args, **kwargs):
#         obj = self.get_object()
#         serializer = self.get_serializer(obj)
#         output = serializer.data
#         return Response(output, status=status.HTTP_200_OK)

#     def put(self, request, *args, **kwargs):
#         obj = self.get_object()
#         serializer = self.get_serializer(obj, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

#     def delete(self, request, *args, **kwargs):
#         obj = self.get_object()
#         try:
#             obj.delete()
#         except ProtectedError:
#             return Response({"error_detail": ["Parent Category can't be deleted, as it is already in relation"]}, status=status.HTTP_423_LOCKED)
#         return Response(status=status.HTTP_204_NO_CONTENT)


class CategoryListView(generics.GenericAPIView):
    permission_classes = [isAdmin]

    def post(self, request, *args, **kwargs):
        serializer = CategorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request, *args, **kwargs):

        queryset = Category.objects.all()
        serializer = CategorySerializer(queryset, many=True)
        output = []
        for data in serializer.data:
            instance = {}
            # parent = ParentCategory.objects.filter(
            #     id=data['parent_category']).get()
            instance.update({"name": data['name'], "is_active": data["is_active"], "keyword": data["keyword"], "id": data['id_category'],
                             "short_code": data['short_code'], "long_description": data["long_description"], "short_description": data["short_description"]})
            if instance not in output:
                output.append(instance)
        return Response(output, status=status.HTTP_200_OK)


class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [isAdmin]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get(self, request, *args, **kwargs):
        obj = self.get_object()
        serializer = self.get_serializer(obj)
        output = serializer.data
        output.update(
            {"parent": {"label": obj.parent_category.name, "value": obj.parent_category.id}})
        return Response(output, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        obj = self.get_object()
        serializer = self.get_serializer(obj, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        try:
            obj.delete()
        except ProtectedError:
            return Response({"error_detail": ["Category can't be deleted, as it is already in relation"]}, status=status.HTTP_423_LOCKED)
        return Response(status=status.HTTP_204_NO_CONTENT)


class ManufacturerListView(generics.GenericAPIView):
    permission_classes = [isAdmin]

    def post(self, request, *args, **kwargs):
        serializer = ManufacturerSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def get(self, request, *args, **kwargs):
        if 'drop' in request.query_params:
            output = []
            queryset = Manufacturer.objects.all()
            serializer = ManufacturerSerializer(queryset, many=True)
            for data in serializer.data:
                instance = {}
                instance.update({"label": data['name'], "value": data['id']})
                if instance not in output:
                    output.append(instance)
            return Response(output, status=status.HTTP_200_OK)
        queryset = Manufacturer.objects.all()
        serializer = ManufacturerSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ManufacturerDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [isAdmin]
    queryset = Manufacturer.objects.all()
    serializer_class = ManufacturerSerializer

    def get(self, request, *args, **kwargs):
        obj = self.get_object()
        serializer = self.get_serializer(obj)
        output = serializer.data
        return Response(output)

    def put(self, request, *args, **kwargs):
        obj = self.get_object()
        serializer = self.get_serializer(obj, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data,)

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        try:
            obj.delete()
        except ProtectedError:
            return Response({"error_detail": ["Manufacturer can't be deleted, as it is already in relation"]}, status=status.HTTP_423_LOCKED)
        return Response(status=status.HTTP_204_NO_CONTENT)


class BrandListView(generics.GenericAPIView):
    permission_classes = [isAdmin]

    def post(self, request, *args, **kwargs):
        serializer = BrandSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def get(self, request, *args, **kwargs):
        if 'drop' in request.query_params:
            output = []
            queryset = Brand.objects.all()
            serializer = BrandSerializer(queryset, many=True)
            for data in serializer.data:
                instance = {}
                instance.update({"label": data['name'], "value": data['id']})
                if instance not in output:
                    output.append(instance)
            return Response(output, status=status.HTTP_200_OK)
        queryset = Brand.objects.all()
        serializer = BrandSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class BrandDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [isAdmin]
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer

    def get(self, request, *args, **kwargs):
        obj = self.get_object()
        serializer = self.get_serializer(obj)
        output = serializer.data
        return Response(output)

    def put(self, request, *args, **kwargs):
        obj = self.get_object()
        serializer = self.get_serializer(obj, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data,)

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        try:
            obj.delete()
        except ProtectedError:
            return Response({"error_detail": ["Item can't be deleted, as it is already in relation"]}, status=status.HTTP_423_LOCKED)
        return Response(status=status.HTTP_204_NO_CONTENT)


class UnitListView(generics.GenericAPIView):
    permission_classes = [isAdmin]

    def post(self, request, *args, **kwargs):
        serializer = UnitSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def get(self, request, *args, **kwargs):
        if 'drop' in request.query_params:
            output = []
            queryset = Unit.objects.all()
            serializer = UnitSerializer(queryset, many=True)
            for data in serializer.data:
                instance = {}
                instance.update({"label": data['name'], "value": data['id']})
                if instance not in output:
                    output.append(instance)
            return Response(output, status=status.HTTP_200_OK)
        queryset = Unit.objects.all()
        serializer = UnitSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UnitDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [isAdmin]
    queryset = Unit.objects.all()
    serializer_class = UnitSerializer

    def get(self, request, *args, **kwargs):
        obj = self.get_object()
        serializer = self.get_serializer(obj)
        output = serializer.data
        return Response(output)

    def put(self, request, *args, **kwargs):
        obj = self.get_object()
        serializer = self.get_serializer(obj, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data,)

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        try:
            obj.delete()
        except ProtectedError:
            return Response({"error_detail": ["Item can't be deleted, as it is already in relation"]}, status=status.HTTP_423_LOCKED)
        return Response(status=status.HTTP_204_NO_CONTENT)


class SalesAccountListView(generics.GenericAPIView):
    permission_classes = [isAdmin]

    def post(self, request, *args, **kwargs):
        serializer = SalesAccountSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def get(self, request, *args, **kwargs):
        if 'drop' in request.query_params:
            output = []
            queryset = SalesAccount.objects.all()
            serializer = SalesAccountSerializer(queryset, many=True)
            for data in serializer.data:
                instance = {}
                instance.update({"label": data['name'], "value": data['id']})
                if instance not in output:
                    output.append(instance)
            return Response(output, status=status.HTTP_200_OK)
        queryset = SalesAccount.objects.all()
        serializer = SalesAccountSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SalesAccountDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [isAdmin]
    queryset = SalesAccount.objects.all()
    serializer_class = SalesAccountSerializer

    def get(self, request, *args, **kwargs):
        obj = self.get_object()
        serializer = self.get_serializer(obj)
        output = serializer.data
        return Response(output)

    def put(self, request, *args, **kwargs):
        obj = self.get_object()
        serializer = self.get_serializer(obj, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data,)

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        try:
            obj.delete()
        except ProtectedError:
            return Response({"error_detail": ["Item can't be deleted, as it is already in relation"]}, status=status.HTTP_423_LOCKED)
        return Response(status=status.HTTP_204_NO_CONTENT)


class PurchaseAccountListView(generics.GenericAPIView):
    permission_classes = [isAdmin]

    def post(self, request, *args, **kwargs):
        serializer = PurchaseAccountSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def get(self, request, *args, **kwargs):
        if 'drop' in request.query_params:
            output = []
            queryset = PurchaseAccount.objects.all()
            serializer = PurchaseAccountSerializer(queryset, many=True)
            for data in serializer.data:
                instance = {}
                instance.update({"label": data['name'], "value": data['id']})
                if instance not in output:
                    output.append(instance)
            return Response(output, status=status.HTTP_200_OK)
        queryset = PurchaseAccount.objects.all()
        serializer = PurchaseAccountSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PurchaseAccountDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [isAdmin]
    queryset = PurchaseAccount.objects.all()
    serializer_class = PurchaseAccountSerializer

    def get(self, request, *args, **kwargs):
        obj = self.get_object()
        serializer = self.get_serializer(obj)
        output = serializer.data
        return Response(output)

    def put(self, request, *args, **kwargs):
        obj = self.get_object()
        serializer = self.get_serializer(obj, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data,)

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        try:
            obj.delete()
        except ProtectedError:
            return Response({"error_detail": ["Item can't be deleted, as it is already in relation"]}, status=status.HTTP_423_LOCKED)
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class BannerListView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    queryset = Banner.objects.all()
    serializer_class = BannerSerializer

    def post(self, request, *args, **kwargs):
        request.data.update({"created_by": request.user.pk})
        serializer = BannerSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data,status=status.HTTP_201_CREATED)

    def get(self, request, *args, **kwargs):
        if 'drop' in request.query_params:
            output = []
            queryset = Banner.objects.all()
            serializer = BannerSerializer(queryset, many=True)
            for data in serializer.data:
                instance = {}
                instance.update({"label": data['banner_name'], "value": data['banner_id']})
                if instance not in output:
                    output.append(instance)
            return Response(output, status=status.HTTP_200_OK)
        queryset = Banner.objects.all()
        serializer = BannerSerializer(queryset, many=True, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class BannerDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [isAdmin]
    queryset = Banner.objects.all()
    serializer_class = BannerSerializer

    def get(self, request, *args, **kwargs):
        obj = self.get_object()
        serializer = self.get_serializer(obj, context={"request": request})
        output = serializer.data
        output.update({"created_by": obj.created_by.username,
                       "updated_by": obj.updated_by.username if obj.updated_by != None else None})
        return Response(output)

    def put(self, request, *args, **kwargs):
        obj = self.get_object()
        data = request.data.copy()
        if (isinstance(data['banner_img'], str)):
            try:
                obj.banner_name = data['banner_name']
                obj.banner_description = data['banner_description']
                obj.banner_status = True if data['banner_status'] == 'true' or data[
                    'banner_status'] == '1' or data['banner_status'] == 1 else False
                obj.updated_by = request.user
                obj.updated_on = datetime.now(tz=timezone.utc)
                obj.save()
                serializer = self.get_serializer(obj)
                return Response(serializer.data)
            except IntegrityError:
                return Response({"error_detail": [
                                "Banner with this banner name already exists."]}, status=status.HTTP_400_BAD_REQUEST)
        request.data.update({"updated_by": request.user.pk,
                            "updated_on": datetime.now(tz=timezone.utc), "created_by": obj.created_by.pk})
        serializer = self.get_serializer(obj, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data,status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        try:
            obj.delete()
        except ProtectedError:
            return Response({"error_detail": ["Item can't be deleted, as it is already in relation"]}, status=status.HTTP_423_LOCKED)
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class OfferSlideListView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    queryset = OfferSlide.objects.all()
    serializer_class = OfferSlideSerializer

    def post(self, request, *args, **kwargs):
        request.data.update({"created_by": request.user.pk})
        serializer = OfferSlideSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data,status=status.HTTP_201_CREATED)

    def get(self, request, *args, **kwargs):
        if 'drop' in request.query_params:
            output = []
            queryset = OfferSlide.objects.all()
            serializer = OfferSlideSerializer(queryset, many=True)
            for data in serializer.data:
                instance = {}
                instance.update({"label": data['offer_slider_content'], "value": data['offer_slider_id']})
                if instance not in output:
                    output.append(instance)
            return Response(output, status=status.HTTP_200_OK)
        queryset = OfferSlide.objects.all()
        serializer = OfferSlideSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class OfferSlideDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [isAdmin]
    queryset = OfferSlide.objects.all()
    serializer_class = OfferSlideSerializer

    def get(self, request, *args, **kwargs):
        obj = self.get_object()
        serializer = self.get_serializer(obj)
        output = serializer.data
        output.update({"created_by": obj.created_by.username,
                       "updated_by": obj.updated_by.username if obj.updated_by != None else None})
        return Response(output)

    def put(self, request, *args, **kwargs):
        obj = self.get_object()
        request.data.update({"updated_by": request.user.pk,
                            "updated_on": datetime.now(tz=timezone.utc), "created_by": obj.created_by.pk})
        serializer = self.get_serializer(obj, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data,status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        try:
            obj.delete()
        except ProtectedError:
            return Response({"error_detail": ["Item can't be deleted, as it is already in relation"]}, status=status.HTTP_423_LOCKED)
        return Response(status=status.HTTP_204_NO_CONTENT)


class GridItemListView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    queryset = GridItem.objects.all()
    serializer_class = GridItemSerializer

    def post(self, request, *args, **kwargs):
        request.data.update({"created_by": request.user.pk})
        serializer = GridItemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data,status=status.HTTP_201_CREATED)

    def get(self, request, *args, **kwargs):
        if 'drop' in request.query_params:
            output = []
            queryset = GridItem.objects.all()
            serializer = GridItemSerializer(queryset, many=True)
            for data in serializer.data:
                instance = {}
                instance.update({"label": data['grid_item_name'], "value": data['grid_item_id']})
                if instance not in output:
                    output.append(instance)
            return Response(output, status=status.HTTP_200_OK)
        queryset = GridItem.objects.all()
        serializer = GridItemSerializer(queryset, many=True, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class GridItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [isAdmin]
    queryset = GridItem.objects.all()
    serializer_class = GridItemSerializer

    def get(self, request, *args, **kwargs):
        obj = self.get_object()
        serializer = self.get_serializer(obj, context={"request": request})
        output = serializer.data
        output.update({"created_by": obj.created_by.username,
                       "updated_by": obj.updated_by.username if obj.updated_by != None else None})
        return Response(output)

    def put(self, request, *args, **kwargs):
        obj = self.get_object()
        data = request.data.copy()
        if (isinstance(data['image'], str)):
            try:
                obj.grid_item_name = data['grid_item_name']
                obj.status = True if data['status'] == 'true' or data[
                    'status'] == '1' or data['status'] == 1 else False
                obj.grid_title=data['grid_title']
                obj.grid_content=data['grid_content']
                obj.updated_by = request.user
                obj.updated_on = datetime.now(tz=timezone.utc)
                obj.save()
                serializer = self.get_serializer(obj)
                return Response(serializer.data)
            except IntegrityError:
                return Response({"error_detail": [
                                "Grid with this Grid item Name already exists."]}, status=status.HTTP_400_BAD_REQUEST)
        request.data.update({"updated_by": request.user.pk,
                            "updated_on": datetime.now(tz=timezone.utc), "created_by": obj.created_by.pk})
        serializer = self.get_serializer(obj, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data,status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        try:
            obj.delete()
        except ProtectedError:
            return Response({"error_detail": ["Item can't be deleted, as it is already in relation"]}, status=status.HTTP_423_LOCKED)
        return Response(status=status.HTTP_204_NO_CONTENT)

