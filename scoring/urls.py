from django.urls import path
from .import views

urlpatterns = [
    path('scoring/', views.scoring, name='scoring'),

    path('scoring/database', views.database_tables, name='scoring_database'),
    path('scoring/archers/', views.archers, name='scoring_archers' )
]
