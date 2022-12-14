"""plantpal URL Configuration

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
from django.conf.urls import include
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from rest_framework import routers
from plantpalapi.views import register_user, login_user, PlantPalView, SwapView, PlantView, WaterSpanView, SunTypeView

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'pals', PlantPalView, 'pal')
router.register(r'swaps', SwapView, 'swap')
router.register(r'plants', PlantView, 'plant')
router.register(r'waterspans', WaterSpanView, 'waterspan')
router.register(r'suntypes', SunTypeView, 'suntype')

urlpatterns = [
    path('', include(router.urls)),
    path('register', register_user),
    path('login', login_user),
    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
