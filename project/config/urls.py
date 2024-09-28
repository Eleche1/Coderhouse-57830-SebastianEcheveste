"""
URL configuration for config project.

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
from reservas import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path("cliente/list", views.cliente_list, name="cliente_list"),
    path("cancha/list", views.cancha_list, name="cancha_list"),
    path("reserva/list", views.reserva_list, name="reserva_list"),
    path("cliente/create", views.cliente_create, name="cliente_create"),
    path("cancha/create", views.cancha_create, name="cancha_create"),
    path("reserva/create", views.reserva_create, name="reserva_create"),
    path("cliente/<int:pk>/editar/", views.cliente_update, name="cliente_update"),
    path("cliente/<int:pk>/eliminar/", views.cliente_delete, name="cliente_delete"),
    path("cancha/<int:pk>/editar/", views.cancha_update, name="cancha_update"),
    path("cancha/<int:pk>/eliminar/", views.cancha_delete, name="cancha_delete"),
    path("reserva/<int:pk>/editar/", views.reserva_update, name="reserva_update"),
    path("reserva/<int:pk>/eliminar/", views.reserva_delete, name="reserva_delete"),
    path("login/", views.user_login, name="login"),
    path("register/", views.user_register, name="register"),
    path("profile/", views.profile, name="profile"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("about/", views.about, name="about"),
]
