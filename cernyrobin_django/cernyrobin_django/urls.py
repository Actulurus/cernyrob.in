"""
URL configuration for cernyrobin_django project.

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
from django.urls import path

from cernyrobin_app import views as cernyrobin
from api import views as api

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", cernyrobin.home),
    path("home/", cernyrobin.home),
    path("clicker/", cernyrobin.clicker_page),
    path("login/", cernyrobin.login_page),

    path("login/submit/", cernyrobin.login_submit, name="login_submit"),
    path("clicker/add_click", cernyrobin.add_click, name="add_click"),
    path("get_user_data/", cernyrobin.get_user_data, name="get_user_data"),
    path("get_all_data/", cernyrobin.get_all_data, name="get_all_data"),

    path("api/kafka/", api.kafka, name="kafka") # i want this to have a subdomain called api
]
