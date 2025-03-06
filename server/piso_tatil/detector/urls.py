from django.urls import path
from .views import home, detect_piso_tatil

urlpatterns = [
    path('', home, name='home'),
    path('api/detectar/', detect_piso_tatil, name='detect_piso_tatil'),
]
