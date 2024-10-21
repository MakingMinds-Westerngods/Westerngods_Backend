from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractUser
from . import file_save
from dateutil.relativedelta import relativedelta


# Accounts , access related models
# User model is used to store Users ; to be used as basic auth model for authentication of both admin and customers
class User(AbstractUser):
    is_customer = models.BooleanField(default=False)
    is_adminuser = models.BooleanField(default=False)
    account_expiry = models.DateField(blank=True, null=True)
    first_name = models.CharField(max_length=45, null=True, blank=True)
    last_name = models.CharField(max_length=45, null=True, blank=True)
    email = models.EmailField(unique=True)
    pass_updated = models.DateTimeField(blank=True, null=True, default=None)

    def __str__(self) -> str:
        return 'User - ' + str(self.pk)

    LOGGING_IGNORE_FIELDS = ('password', 'first_name',
                             'last_name', 'last_login')

    class Meta:
        db_table = 'users'
        constraints = [
            models.CheckConstraint(violation_error_message='isAdmin and isCustomer values cannot be same', name='Admin and Customer values cannot be same', check=~(
                models.Q)(is_customer=models.F('is_adminuser'))),
            models.CheckConstraint(violation_error_message='Customer cannot become a staff',
                                   name='Customer cannot become a staff', check=~models.Q(models.Q(is_customer=True), models.Q(is_staff=True))),
            models.CheckConstraint(violation_error_message='Customer cannot become superuser',
                                   name='Customer cannot become superuser', check=~models.Q(models.Q(is_customer=True), models.Q(is_superuser=True))),
        ]

class CustomerOTP(models.Model):

    OTP_FOR = (
        ("1", "Login OTP"),
        ("2", "Password Reset OTP"),
        ("3", "Profile Email Change OTP"),
        ("4", "Email Verify OTP"),
    )

    id_otp = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(
        'User', on_delete=models.CASCADE,limit_choices_to={'is_customer': True}, related_name='cus_otp_set')
    email_id = models.EmailField()
    otp_code = models.CharField(
        max_length=6)
    creation_time = models.DateTimeField(default=timezone.now)
    expiry = models.DateTimeField()
    otp_for = models.CharField(choices=OTP_FOR, max_length=1)

    def __str__(self) -> str:
        return 'Customer OTP - ' + str(self.pk)

    class Meta:
        db_table = 'customer_otp'
    # LOG IGNORE THIS MODEL

# Admin model is used to store Admin users
class Admin(models.Model):
    adminid = models.AutoField(primary_key=True)
    name = models.CharField(
        max_length=100)
    user = models.OneToOneField(
        'User', on_delete=models.PROTECT, limit_choices_to={'is_adminuser': True}, related_name='admin')
    admin_email_verified = models.BooleanField(default=False)

    def __str__(self) -> str:
        return 'Admin User - ' + str(self.pk)

    class Meta:
        db_table = 'admin'


# Admin OTP model is used to store Email OTPs of user
class AdminOTP(models.Model):

    OTP_FOR = (
        ("0", "Password Reset OTP"),
        ("1", "Profile Email Change OTP"),
        ("2", "Email Verify OTP"),
    )

    id_otp = models.BigAutoField(primary_key=True)
    admin = models.ForeignKey(
        'Admin', on_delete=models.CASCADE, related_name='otp_set')
    email_id = models.EmailField()
    otp_code = models.CharField(
        max_length=6)
    creation_time = models.DateTimeField(default=timezone.now)
    expiry = models.DateTimeField()
    otp_for = models.CharField(choices=OTP_FOR, max_length=1)

    def __str__(self) -> str:
        return 'Admin User OTP - ' + str(self.pk)

    class Meta:
        db_table = 'admin_otp'
    # LOG IGNORE THIS MODEL


# Settings model is used to store some global settings
class Settings(models.Model):
    id_settings = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    value = models.CharField(max_length=255)

    def __str__(self) -> str:
        return 'Settings - ' + str(self.pk)

    class Meta:
        db_table = 'settings'


# menu model is used to store the admin menu - side menus
class AdminMenu(models.Model):
    text = models.CharField(max_length=45)
    link = models.CharField(max_length=75,  unique=True, error_messages={
                            "unique": "Menu with this link already exists"})
    icon = models.CharField(max_length=85, null=True, blank=True)
    parent = models.ForeignKey(
        'AdminMenu', null=True, blank=True, default=None, on_delete=models.SET_NULL)
    order = models.IntegerField(default=0)
    active = models.BooleanField(default=True)
    sub = models.BooleanField(default=False)
    title = models.CharField(max_length=125, null=True)

    def __str__(self) -> str:
        return 'Admin Menu - ' + str(self.pk)

    class Meta:
        db_table = "admin_menu"


# Admin menu access model is used to store the permissions of admin on individual menu items - Admin side menu
class AdminMenuAccess(models.Model):
    id_admin_menu_access = models.AutoField(primary_key=True)
    admin = models.ForeignKey('Admin',
                              on_delete=models.CASCADE,
                              related_name="menu_access")
    menu = models.ForeignKey('AdminMenu',
                             on_delete=models.CASCADE,
                             related_name="access_admin")
    view = models.BooleanField(default=False)
    add = models.BooleanField(default=False)
    edit = models.BooleanField(default=False)
    delete = models.BooleanField(default=False)

    def __str__(self) -> str:
        return 'Admin Menu Access - ' + str(self.pk)

    class Meta:
        db_table = "admin_menu_access"


class LoginDetails(models.Model):
    detail_id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey('User',
                             on_delete=models.CASCADE)
    is_mobile = models.BooleanField(default=False)
    is_tablet = models.BooleanField(default=False)
    is_touch_capable = models.BooleanField(default=False)
    is_pc = models.BooleanField(default=False)
    is_bot = models.BooleanField(default=False)
    browser_fam = models.CharField(max_length=50)
    browser_ver = models.CharField(max_length=50)
    os_fam = models.CharField(max_length=50)
    os_ver = models.CharField(max_length=50)
    device_fam = models.CharField(max_length=50)
    device_brand = models.CharField(max_length=50, null=True)
    ip_address = models.CharField(max_length=50)
    signin_time = models.DateTimeField()

    def __str__(self) -> str:
        return 'Login Device Details - ' + str(self.pk)

    class Meta:
        db_table = "login_details"
