from django.urls import path
from knox.views import LogoutView

from accounts.views import (AdminCRUDAPI, AdminChange, AdminChangePassword, AdminInfo, AdminMenuDetails, AdminMenuFetch,
                            AdminMenuList, AdminOTPCreate, AdminOTPVerify, AdminResetPassword, AdminSignInView, ChangesLogAPI,
                            CheckAcess, CheckTokenAPI, EditAdmin, loginsessionView, CustomerSigninOTPCreate, CustomerSigninOTPVerify,
                            CustomerSignupView)


urlpatterns = [
    path('auth/admin_signin/', AdminSignInView.as_view(), name='admin_sign_in'),
    path('auth/admin_signout/', LogoutView.as_view(), name='admin_sign_out'),
    path('auth/check_token/', CheckTokenAPI.as_view(),
         name='check_token_is_valid'),
    path('auth/admin_info/', AdminInfo.as_view(),
         name='get_admin_info'),
    path('auth/login_det/', loginsessionView.as_view(), name='login_det'),
    
    path('auth/cus_register/', CustomerSignupView.as_view(), name='cus_register'),
    path('auth/cus_login_otp_create/', CustomerSigninOTPCreate.as_view(), name='cus_login_otp_create'),
    path('auth/cus_login_otp_verify/', CustomerSigninOTPVerify.as_view(), name='cus_login_otp_verify'),
    path('auth/cus_signout/', LogoutView.as_view(), name='cus_sign_out'),
    
    path('admin_change_pass/', AdminChangePassword.as_view(),
         name='change_admin_pass'),
    path('admin_change/', AdminChange.as_view(), name='change_admin_details'),
    path('admin_edit/', EditAdmin.as_view(), name='edit_admin'),
    path('admin_create_otp/', AdminOTPCreate.as_view(),
         name='admin_create_otp'),
    path('admin_verify_otp/', AdminOTPVerify.as_view(),
         name='admin_verify_otp'),
    path('admin_reset_pass/', AdminResetPassword.as_view(),
         name='admin_reset_passwd'),
    path('admins/', AdminCRUDAPI.as_view(),
         name='listcreate_admin'),
    path('admins/<int:pk>/', AdminCRUDAPI.as_view(),
         name='fetchupdatedelete_admin'),
    path('access_check/', CheckAcess.as_view(),
         name='check_admin_access'),
    path('logs/', ChangesLogAPI.as_view(),
         name='logs_list_view'),
    path('adminmenu/', AdminMenuList.as_view(),
         name='listcreate_adminmenu'),
    path('adminmenu/<int:pk>/', AdminMenuDetails.as_view(),
         name='fetchupdatedelete_adminmenu_entry'),
    path('fetchmenu/', AdminMenuFetch.as_view(),
         name='fetch_admin_menu'),

]


# DUMMY
