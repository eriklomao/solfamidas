"""solfamidas URL Configuration

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

from home.views import principal
from clasificacion.views import clasificacion
from mercado.views import mercado
from equipo.views import equipo, addJugador, delJugador, crear_equipo, addPlayer, delPlayer
from acceso.views import loginPage, registerPage, logoutUser

urlpatterns = [
    path('admin/', admin.site.urls),

    #Urls principales de la web

    path('', principal, name='principal'),
    path('clasificacion/', clasificacion, name='clasificacion'),
    path('mercado/', mercado, name='mercado'),
    path('equipo/', equipo, name='equipo'),

    #Urls de compra y venta de jugadores

    path('comprar/', addJugador, name='addJugador'),
    path('vender/', delJugador, name='delJugador'),

    #Urls de gestion de usuarios

    path('login/', loginPage, name='login'),
    path('register/', registerPage, name='register'),
    path('logout/', logoutUser, name='logout'),

    #Urls auxiliares

    path('equipo/crear_equipo/', crear_equipo, name='crear_equipo'),
    path('equipo/add_player/', addPlayer, name='addPlayer'),
    path('equipo/del_player/', delPlayer, name='delPlayer'),

]
