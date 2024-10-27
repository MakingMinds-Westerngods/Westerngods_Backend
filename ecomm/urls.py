from django.urls import path

from .views import (ProductListView, TshirtListView, HoodieListView, CategoryListView, NavMenuList, 
                    CategoryProductsList, ItemDetailsView,ItemAllImagesView, WishlistListView, 
                    wishlistDetailView, ItemImagesHomeView, SearchItemsView)

urlpatterns = [
    path('productlist/', ProductListView.as_view()),
    path('tshirtlist/', TshirtListView.as_view()),
    path('hoodie_list/', HoodieListView.as_view()),
    path('categories/', CategoryListView.as_view()),
    path('navbar_menu/', NavMenuList.as_view()),
    path('items/<int:pk>/', CategoryProductsList.as_view()),
    path('item/<int:pk>/', ItemDetailsView.as_view()),
    path("item_images/",ItemAllImagesView.as_view()),
    path("home_item_images/",ItemImagesHomeView.as_view()),
    path('wishlist/', WishlistListView.as_view()),
    path('wishlist/<int:pk>/', wishlistDetailView.as_view()),
    path('search_items/', SearchItemsView.as_view()),

]