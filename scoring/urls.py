from django.urls import path
from .import views

urlpatterns = [
    path('scoring/', views.scoring, name='scoring'),

    path('scoring/archers/', views.archers, name='archers' )
]
