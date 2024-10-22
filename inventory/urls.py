from django.urls import path
from .views import( ItemListView,ItemDetailView,UsersiteItemListView,UsersiteCategoryView,
                   SendOTPView,VerifyOTPView,BagDetailView,BagListView)



urlpatterns = [
    path('item/', ItemListView.as_view()),
    path('item/<int:pk>/', ItemDetailView.as_view()),  
    path('bag/', BagListView.as_view()),
    path('bag/<int:pk>/', BagDetailView.as_view()), 
    path('customeritemview/', UsersiteItemListView.as_view(), name='customerview'), 
    path('customercategoryview/', UsersiteCategoryView.as_view(), name='customerview'), 
    path('generate-otp/', SendOTPView.as_view(), name='generate_otp'),
    path('verify-otp/', VerifyOTPView.as_view(), name='verify_otp'),
]

