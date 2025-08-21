"""
URL configuration for Smartcityconnect project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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

from smartcity.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    
    path('admin-dj/', admin.site.urls),
    path('ServiceProviderRegistration/',ServiceRegistration,name='ServiceProviderRegistration'),
    path('CustomerReg/',CustomerReg,name='CustomerReg'),
    path('Home/',Home,name='Home'),
    path('About',About,name='About'),
    path('Loginpage/',Loginpage,name='Loginpage'),
    path('Plumber/',Plumber,name='Plumber'),
    path('logout', logout_view, name='logout'),
    path('jarvis/chat/', jarvis_chat, name='jarvis_chat'),
    path('Electricion/',Electricion,name="Electricion"),
    path('Carpenter/',Carpenter,name='Carpenter'),
    path('Painter/',Painter,name='Painter'),
    path('Welder/',Welder,name="Welder"),
    path('CableProvider/',CableProvider,name='CableProvider'),
    path('Internat/',Internat,name='Internat'),
    path('Groceries/',Groceries,name='Groceries'),
    path('admin/login/', admin_login, name='admin_login'),
    path('admin/dashboard/', dashboard, name='dashboard'),
    path('approve-provider/<int:provider_id>/', approve_provider, name='approve_provider'),
    path('reject-provider/<int:provider_id>/', reject_provider, name='reject_provider'),
    path('service_providers',service_providers,name="service_providers"),
    path('service-providers/edit/<int:provider_id>/', edit_provider, name='edit_provider'),
    path('service-providers/<int:provider_id>/', service_provider_view, name='service_provider_view'),
    path('customers', customers, name='customers'),
    path('customers/<int:customer_id>/',customer_detail, name='customer_detail'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

