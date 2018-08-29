"""Clim_MeteoR URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))  {% url "initialisationPAYS"   %}   , name='initialisationPAYS' 
"""
from django.contrib import admin
from django.urls import path
from gestion import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accueil', views.home),
    path('initialisation/', views.initPays),#Initialisation d'une station
    path('InfoPoste/<str:code>/<str:typestation>/<str:capteur>/', views.infoposte),#Initialisation des capteurs d'une station
    path('Releve/',views.releve), #Soumission de données manuelles SPIEA
    path('Reactualisation/',views.reactualisation), #Reactualisation des donnees en cas de perte/panne
    path('station/<str:codeposte>/',views.affichage), 
    path('recap/ev/<str:codeevenement>/<str:codeposte>/',views.recapevenement),
    path('recap/J/<str:codeposte>/',views.recap),
    path('recap/M/<str:codeposte>/',views.recapMensuel),
    path('rapport/M/<str:date>/<str:codeposte>/',views.rapport),
    path('rapport/A/<str:date>/<str:codeposte>/',views.rapportannuel),

]
