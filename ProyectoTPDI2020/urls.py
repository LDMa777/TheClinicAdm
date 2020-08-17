"""ProyectoTPDI2020 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from ProyectoTPDI2020.views import ingreso, controlLogin, table, edit, delete, add, controlpanelAdmin

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('ingreso/loginSuccess=<str:ingresovalido>', ingreso),
    path('ingreso/', ingreso),
    
    path('table/<str:tablename>/deleteSuccess=<str:deleted>',table),
    path('table/<str:tablename>/addSuccess=<str:added>',table),
    path('table/<str:tablename>/editSuccess=<str:edited>',table),
    path('table/<str:tablename>/',table),
    
    path('edit/<str:tablename>/<str:tableid>',edit),
    path('edit/<str:tablename>/<str:tableid>/makeEdition=<str:makeedit>',edit),

    path('delete/<str:tablename>/<str:tableid>',delete),
    
    path('add/<str:tablename>',add),
    path('add/<str:tablename>/makeAdd=<str:makeadd>',add),
    
    path('controlLogin/', controlLogin),

    path('controlpanelAdmin/', controlpanelAdmin),
]
