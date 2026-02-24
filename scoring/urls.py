from django.urls import path
from .import views

urlpatterns = [
    path('scoring/', views.scoring, name='scoring'),

    path('scoring/register/', views.register, name='scoring_register'),
    path('scoring/my-login', views.my_login, name='scoring_my-login'),
    path('scoring/user-logout', views.user_logout, name='scoring_user-logout'),
    path('scoring/dashboard', views.dashboard, name='scoring_dashboard'),

    path('scoring/database', views.database_tables, name='scoring_database'),

    path('scoring/archers/', views.archers, name='scoring_archers' ),
]
