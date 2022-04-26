# Djanfo
from django.urls import path
from apps.bonos.views import Main, download_bonus

urlpatterns = [
    path('main/', Main.as_view()),
    path('bonus', download_bonus)
]