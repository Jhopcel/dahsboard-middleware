"""
URL configuration for my_dashboard project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from . import views
from django.http import JsonResponse

from .views import (
    login_succes,
    logout_view,
    find_user_view,
    index,
    pdf_wiewer,
    scan
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', login_succes, name='login'),
    path('logout/', logout_view, name='logout'),
    path('', index, name= 'index'),
    path('classify/', find_user_view, name='classify'),
    path('my_pdf/', pdf_wiewer, name='pdf_wiewer'),
    path('scan/', scan, name='scan')
]



# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('dashboard', views.index, name='index'),
#     path('login/', views.login_succes, name='login'),
#     path('logout/', views.logout_succes, name='logout'),
#     path('get_username/', views.get_username, name= 'get_username'),
#     path('', views.scan, name= 'scan'),
#     path('verify_user/', views.verify_user, name='verify_user')
# ]

