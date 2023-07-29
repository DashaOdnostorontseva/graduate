"""
URL configuration for podpisant project.

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
from django.conf.urls.static import static
from django.conf import settings

from documents.views import index, mypodpis, mydocs, mydocsnull, status, validate, choose_cert, write_cert, my_cert, my_cert_null, cert_option, download_file, get_file
from users.views import registration, login, profile, logout


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('myp', mypodpis, name='myp'),
    path('download_file', download_file, name='download_file'),
    path('registration', registration, name='registration'),
    path('login', login, name='login'),
    path('profile', profile, name='profile'),
    path('logout', logout, name='logout'),
    path('mydocs', mydocs, name='mydocs'),
    path('mydocsnull', mydocsnull, name='mydocsnull'),
    path('status/<int:doc_id>', status, name='status'),
    path('validate', validate, name='validate'),
    path('choose_cert', choose_cert, name='choose_cert'),
    path('write_cert', write_cert, name='write_cert'),
    path('my_cert', my_cert, name='my_cert'),
    path('my_cert_null', my_cert_null, name='my_cert_null'),
    path('cert_option', cert_option, name='cert_option'),
    path('get_file', get_file, name='get_file')
]




