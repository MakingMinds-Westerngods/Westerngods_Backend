from rest_framework import serializers
from django.contrib.auth import authenticate
from models_logging.models import Change
from django.core.validators import EmailValidator

from accounts.models import Admin, AdminMenu, User, LoginDetails



class CustomerSignInSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        email_validation = EmailValidator()
        # check username is a Email Address
        try:
            email_validation(data['username'])
            # Find username using the Email address provided
            try:
                username = User.objects.get(email=data['username']).username
                data.update({"username": username})
            except User.DoesNotExist:
                raise serializers.ValidationError(
                    {"error_detail": [
                        "Incorrect username/password"]}
                )
        except:
            pass

        user = authenticate(**data)
        if user:
            if user.is_active:
                if user.is_customer:
                    return user
                raise serializers.ValidationError(
                    {"error_detail": [
                        "Incorrect username/password for Customer"]})
            raise serializers.ValidationError(
                {"error_detail": [
                    "Inactive Account"]})
        raise serializers.ValidationError(
            {"error_detail": [
                "Incorrect username/password"]}
        )

# serializer for Admin sign in validation
class AdminSignInSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        email_validation = EmailValidator()
        # check username is a Email Address
        try:
            email_validation(data['username'])
            # Find username using the Email address provided
            try:
                username = User.objects.get(email=data['username']).username
                data.update({"username": username})
            except User.DoesNotExist:
                raise serializers.ValidationError(
                    {"error_detail": [
                        "Incorrect username/password"]}
                )
        except:
            pass

        user = authenticate(**data)
        if user:
            if user.is_active:
                if user.is_adminuser:
                    return user
                raise serializers.ValidationError(
                    {"error_detail": [
                        "Incorrect username/password for Admin"]})
            raise serializers.ValidationError(
                {"error_detail": [
                    "Inactive Account"]})
        raise serializers.ValidationError(
            {"error_detail": [
                "Incorrect username/password"]}
        )


# serializer for AdminMenu model
class AdminMenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminMenu
        fields = '__all__'


# serializer for Admin model
class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admin
        fields = '__all__'


# serializer for logs - changes
class ChangesLogAPISerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')

    class Meta:
        model = Change
        fields = '__all__'


# <- USER SITE ->
class MemberSignInSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        email_validation = EmailValidator()
        # check username is a Email Address
        try:
            email_validation(data['username'])
            # Find username using the Email address provided
            try:
                username = User.objects.get(email=data['username']).username
                data.update({"username": username})
            except User.DoesNotExist:
                raise serializers.ValidationError(
                    {"error_detail": [
                        "Incorrect username/password saaale"]}
                )
        except:
            pass
        user = authenticate(**data)
        if user:
            if user.is_active:
                if user.is_customer:
                    return user
                raise serializers.ValidationError(
                    {"error_detail": [
                        "Incorrect username/password"]})
            raise serializers.ValidationError(
                {"error_detail": [
                    "Inactive Account"]})
        raise serializers.ValidationError(
            {"error_detail": [
                "Incorrect username/password"]}
        )


class LoginDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoginDetails
        fields = '__all__'
