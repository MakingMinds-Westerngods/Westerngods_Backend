from django.urls import path
from .views import(CategoryListView,CategoryDetailView,ManufacturerDetailView,ManufacturerListView,BrandDetailView,BrandListView,SalesAccountDetailView,SalesAccountListView,
                   PurchaseAccountDetailView,PurchaseAccountListView,UnitListView,UnitDetailView, CountryView,OfferSlideListView,OfferSlideDetailView,
                   CountryDetailsView, StateView, StateDetailsView, DistrictView, DistrictDetailsView, CityView, CityDetailsView,
                   BannerListView,BannerDetailView,GridItemListView,GridItemDetailView)


urlpatterns = [
    path('category/', CategoryListView.as_view()),
    path('category/<int:pk>/', CategoryDetailView.as_view()), 
        
    path('manufacturer/', ManufacturerListView.as_view()),
    path('manufacturer/<int:pk>/', ManufacturerDetailView.as_view()), 
    
    path('brand/', BrandListView.as_view()),
    path('brand/<int:pk>/', BrandDetailView.as_view()),
     
    path('sales_account/', SalesAccountListView.as_view()),
    path('sales_account/<int:pk>/', SalesAccountDetailView.as_view()),
     
    path('purchase_account/', PurchaseAccountListView.as_view()),
    path('purchase_account/<int:pk>/', PurchaseAccountDetailView.as_view()),
  
    path('unit/', UnitListView.as_view()),
    path('unit/<int:pk>/', UnitDetailView.as_view()), 
    
    path('country/', CountryView.as_view()),
    path('country/<int:pk>/', CountryDetailsView.as_view()), 
    
    path('state/', StateView.as_view()),
    path('state/<int:pk>/', StateDetailsView.as_view()), 
    
    path('district/', DistrictView.as_view()),
    path('district/<int:pk>/', DistrictDetailsView.as_view()), 
    
    path('city/', CityView.as_view()),
    path('city/<int:pk>/', CityDetailsView.as_view()), 
        
    path('bannner/', BannerListView.as_view()),
    path('bannner/<int:pk>/', BannerDetailView.as_view()),

    path('offerslide/', OfferSlideListView.as_view()),
    path('offerslide/<int:pk>/', OfferSlideDetailView.as_view()),

    path('grid_item/', GridItemListView.as_view()),
    path('grid_item/<int:pk>/', GridItemDetailView.as_view()),

]

