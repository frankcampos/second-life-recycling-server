"""second_life_recycling URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from rest_framework import routers
from second_life_recycling_api.views import check_user, register_user, RecyclableItemsViewSet, ShoppingCartView, VendorsView, CategoriesView


router = routers.DefaultRouter(trailing_slash=False)
router.register(r'recyclable_items', RecyclableItemsViewSet)
router.register(r'cart', ShoppingCartView, 'cart')
router.register(r'vendors', VendorsView, 'vendors')
router.register(r'categories', CategoriesView, 'categories')

urlpatterns = [
    path('', include(router.urls)),
    path("admin/", admin.site.urls),
    path("register", register_user),
    path('checkuser', check_user, name='check_user'),
    
]
