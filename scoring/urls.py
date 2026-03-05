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
    path('scoring/agegroup/create/', views.create_agegroup, name='scoring_agegroup_create'),

    # Archer
    path('scoring/archers/', views.archers, name='scoring_archers' ),
    path('scoring/archer/create/', views.create_archer, name='scoring_archer_create' ),

    # Category
    path('scoring/categories', views.categories, name='scoring_categories'),
    path('scoring/category/create', views.create_category, name='scoring_category_create'),

    # Club
    path('scoring/clubs/', views.clubs, name='scoring_clubs' ),
    path('scoring/club/create/', views.create_club, name='scoring_club_create' ),

    # Competition
    path('scoring/competitions/', views.competitions, name='scoring_competitions' ),
    path('scoring/competition/create/', views.create_competition, name='scoring_competition_create' ),

    # Discipline
    path('scoring/disciplines/', views.disciplines, name='scoring_disciplines' ),
    path('scoring/discipline/create/', views.create_discipline, name='scoring_discipline_create' ),

    # Round
    path('scoring/rounds/', views.rounds, name='scoring_rounds' ),
    path('scoring/round/create/', views.create_round, name='scoring_round_create' ),

    # Score
    path('scoring/scores/', views.scores, name='scoring_scores' ),
    path('scoring/score/create/', views.create_score, name='scoring_score_create' ),

    # ScoringSheet
    path('scoring/scoringsheets/', views.scoringsheets, name='scoring_scoringsheets' ),
    path('scoring/scoringsheet/create/', views.create_scoringsheet, name='scoring_scoringsheet_create' ),

    # TargetFace
    path('scoring/targetfaces/', views.targetfaces, name='scoring_targetfaces' ),
    path('scoring/targetface/create/', views.create_targetface, name='scoring_targetface_create' ),

    # Team
    path('scoring/teams/', views.teams, name='scoring_teams' ),
    path('scoring/team/create/', views.create_team, name='scoring_team_create' ),
]
