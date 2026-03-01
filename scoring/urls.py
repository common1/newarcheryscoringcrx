from django.urls import path
from .import views

urlpatterns = [
    path('scoring/', views.scoring, name='scoring'),

    path('scoring/register/', views.register, name='scoring_register'),
    path('scoring/my-login', views.my_login, name='scoring_my-login'),
    path('scoring/user-logout', views.user_logout, name='scoring_user-logout'),
    path('scoring/dashboard', views.dashboard, name='scoring_dashboard'),
    path('scoring/database', views.database_tables, name='scoring_database'),

    # CRUD

    # Agegroup
    path('scoring/agegroups/', views.agegroups, name='scoring_agegroups'),

    # Archer
    path('scoring/archers/', views.archers, name='scoring_archers' ),

    # Category
    path('scoring/categories', views.categories, name='scoring_categories'),

    # Club
    path('scoring/clubs/', views.clubs, name='scoring_clubs' ),

    # Competition
    path('scoring/competitions/', views.competitions, name='scoring_competitions' ),

    # Discipline
    path('scoring/disciplines/', views.disciplines, name='scoring_disciplines' ),

    # Round
    path('scoring/rounds/', views.rounds, name='scoring_rounds' ),

    # Score
    path('scoring/scores/', views.scores, name='scoring_scores' ),

    # ScoringSheet
    path('scoring/scoringsheets/', views.scoringsheets, name='scoring_scoringsheets' ),

    # TargetFace
    path('scoring/targetfaces/', views.targetfaces, name='scoring_targetfaces' ),

    # Team
    path('scoring/teams/', views.teams, name='scoring_teams' ),

]
