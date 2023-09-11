"""
URL configuration for ProjectFinal project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.authtoken.views import obtain_auth_token # <-- NEW

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('admin_datta.urls')),
    path('', include('django_dyn_dt.urls')),  # <-- NEW: API routing rules
    path('', include('general.urls')),
    path('product/', include('product.urls')),
    path('purchase/', include('purchase.urls')),
    path('account/', include('account.urls')),
    path('cart/', include('cart.urls')),
    path('order/', include('order.urls')),
    path('contract/', include('contract.urls')),
    path("api/", include("api.urls")),        # <-- NEW
    path('login/jwt/', view=obtain_auth_token), # <-- NEW
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
