"""uw_manager URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from app01 import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login.html', views.login),
    path('manager.html', views.manager),
    path('manager/classes', views.manager_classes),
    path('manager/student', views.manager_student),
    path('manager/teacher', views.manager_teacher),
    path('api/add/classes', views.api_add_classes),
    path('api/update/classes', views.api_update_classes),
    path('api/delete/classes', views.api_delete_classes),
    path('api/add/student', views.api_add_student),
    path('api/update/student', views.api_update_student),
    path('api/delete/student', views.api_delete_student),
    path('api/add/teacher', views.api_add_teacher),
    path('api/update/teacher', views.api_update_teacher),
    path('api/delete/teacher', views.api_delete_teacher),
    path('logout', views.logout),
    path('test', views.test),
    path('upload.html', views.upload),
]

